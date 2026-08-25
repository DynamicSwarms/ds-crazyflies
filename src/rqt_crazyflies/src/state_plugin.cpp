
#include "rqt_crazyflies/state_plugin.hpp"
#include <pluginlib/class_list_macros.hpp>
#include <QScrollBar>

namespace rqt_crazyflies
{

StatePlugin::StatePlugin()
: rqt_gui_cpp::Plugin()
{
    setObjectName("StatePlugin");
}

StatePlugin::~StatePlugin()
{
    m_pose_subscription.reset();
    m_link_quality_subscription.reset();
}

void StatePlugin::initPlugin(qt_gui_cpp::PluginContext & context)
{
    m_node = node_;
    m_widget = new QWidget();
    m_ui.setupUi(m_widget);


    m_widget->setWindowTitle("Crazyflie Batteries: (canFly, isFlying, isTumbled)");
    if (context.serialNumber() > 1)
    {
        m_widget->setWindowTitle(
            QString("%1 (%2)").arg(m_widget->windowTitle()).arg(context.serialNumber()));
    }
    context.addWidget(m_widget);
    m_ui.list_widget->setSortingEnabled(true);

    connect(this, &StatePlugin::add_crazyflie_signal, this, &StatePlugin::m_signal_handler_add_crazyflie);
    connect(this, &StatePlugin::console_println_signal, this, &StatePlugin::m_signal_handler_console_println);

    m_pose_subscription = m_node->create_subscription<crazyflie_interfaces::msg::PoseNamedArray>(
        "cf_positions", 10,
        std::bind(&StatePlugin::m_on_positions_update, this, std::placeholders::_1));
    m_link_quality_subscription = m_node->create_subscription<crazyflie_interfaces::msg::CrazyflieLinkQualityArray>(
        "/crazyradio/link_qualities", 10,
        std::bind(&StatePlugin::m_on_link_qualities_update, this, std::placeholders::_1));
}

void StatePlugin::shutdownPlugin()
{
    m_pose_subscription.reset();
    m_link_quality_subscription.reset();
    m_crazyflies.clear();
    m_console_messages.clear();
    m_ui.list_widget->clear();
    m_widget = nullptr;
}


void StatePlugin::m_on_positions_update(const crazyflie_interfaces::msg::PoseNamedArray::SharedPtr msg)
{
    for (const auto& pose : msg->poses) {
        const std::string& frame_id = pose.name;
        // Check if frame_id exists in m_status_frames
        if (frame_id.size() < 3) {
            RCLCPP_WARN(
                rclcpp::get_logger("StatePlugin"),
                "Invalid frame_id: '%s'",
                frame_id.c_str());
            continue;
        }

        int id = std::stoi(frame_id.substr(2)); // Assuming frame_id is like "cf1", "cf2", etc.
        auto it = m_crazyflies.find(id);
        if (it == m_crazyflies.end()) {
            emit add_crazyflie_signal(id);
        } else {
            std::vector<double> position = {pose.pose.position.x, pose.pose.position.y, pose.pose.position.z};
            m_crazyflies[id].connection->set_position(position);
        }
    }
}

void StatePlugin::m_on_link_qualities_update(const crazyflie_interfaces::msg::CrazyflieLinkQualityArray::SharedPtr msg)
{
    for (const auto& quality : msg->link_qualities) {
        int id = quality.id;
        auto it = m_crazyflies.find(id);
        if (it != m_crazyflies.end()) {
            m_crazyflies[id].connection->set_link_quality(quality.link_quality);
        }
    }
}

void StatePlugin::console_println(const std::string& msg)
{
    emit console_println_signal(QString::fromStdString(msg));
}




void
StatePlugin::m_signal_handler_add_crazyflie(int id)
{
    if (m_crazyflies.find(id) != m_crazyflies.end()) {
        return;
    }

    std::shared_ptr<CrazyflieConnection> connection = std::make_shared<CrazyflieConnection>(
        id,
        m_node->get_node_base_interface(),
        m_node->get_node_topics_interface(),
        m_node->get_node_graph_interface(),
        m_node->get_node_services_interface()
    );


    connection->set_console_update_callback([this](const std::string& msg) {
        this->console_println(msg);});

    auto *item = new CrazyflieListWidgetItem(id);
    auto *widget = new CrazyflieStatusWidget(m_ui.list_widget, connection);

    m_crazyflies[id] = {item, widget, connection};

    item->setSizeHint(QSize(500, widget->getHeight()));
    m_ui.list_widget->addItem(item);
    m_ui.list_widget->setItemWidget(item, widget);
    m_ui.list_widget->sortItems();
}


void StatePlugin::m_signal_handler_console_println(const QString &msg)
{
    m_console_messages.push_back(msg);
    if (m_console_messages.size() > 1000) {
        m_console_messages.pop_front();
    }
    QStringList lines;
    for (const auto& line : m_console_messages) {
        lines << line;
    }
    m_ui.console_textedit->setPlainText(lines.join("\n"));
    m_ui.console_textedit->verticalScrollBar()->setValue(m_ui.console_textedit->verticalScrollBar()->maximum());
}

void StatePlugin::saveSettings(
    qt_gui_cpp::Settings & plugin_settings,
    qt_gui_cpp::Settings & instance_settings) const
{
    (void)plugin_settings;
    (void)instance_settings;
    // Save the state of the UI elements
}

void StatePlugin::restoreSettings(
    const qt_gui_cpp::Settings & plugin_settings,
    const qt_gui_cpp::Settings & instance_settings)
{
    (void)plugin_settings;
    (void)instance_settings;
    // Restore the state of the UI elements
}

} // namespace rqt_crazyflies



PLUGINLIB_EXPORT_CLASS(rqt_crazyflies::StatePlugin, rqt_gui_cpp::Plugin)
