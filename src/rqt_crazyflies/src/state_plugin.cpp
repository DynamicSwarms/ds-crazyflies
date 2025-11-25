
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
    m_update_timer->stop();
    delete m_update_timer;
    for (auto& pair : m_status_frames) {
        delete pair.second;
    }
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

    m_update_timer = new QTimer(m_widget);
    connect(m_update_timer, &QTimer::timeout, this, &StatePlugin::m_on_update_timer);
    m_update_timer->start(200);

    connect(this, &StatePlugin::m_status_frame_add, this, &StatePlugin::m_add_status_frame);
    connect(this, &StatePlugin::m_console_println, this, &StatePlugin::m_on_console_println);

    m_pose_subscription = m_node->create_subscription<crazyflie_interfaces::msg::PoseStampedArray>(
        "cf_positions", 10,
        std::bind(&StatePlugin::m_on_positions_update, this, std::placeholders::_1));
    m_link_quality_subscription = m_node->create_subscription<crtp_interfaces::msg::CrtpLinkQualities>(
        "/crazyradio/crtp_link_qualities", 10,
        std::bind(&StatePlugin::m_on_link_qualities_update, this, std::placeholders::_1));
}

void StatePlugin::m_on_positions_update(const crazyflie_interfaces::msg::PoseStampedArray::SharedPtr msg)
{
    for (const auto& pose : msg->poses) {
        const std::string& frame_id = pose.header.frame_id;
        // Check if frame_id exists in m_status_frames
        int id = std::stoi(frame_id.substr(2)); // Assuming frame_id is like "cf1", "cf2", etc.
        auto it = m_status_frames.find(id);
        if (it == m_status_frames.end()) {
            m_status_frames[id] = nullptr;
            emit m_status_frame_add(id);
        } else {
            if (it->second != nullptr)
                it->second->position_update(pose.pose.position.x,
                                             pose.pose.position.y,
                                             pose.pose.position.z);
        }
    }
}

void StatePlugin::m_on_link_qualities_update(const crtp_interfaces::msg::CrtpLinkQualities::SharedPtr msg)
{
    for (const auto& quality : msg->link_qualities) {
        int id = quality.link.address[4] ;
        auto it = m_status_frames.find(id);
        if (it != m_status_frames.end() && it->second != nullptr) {
            it->second->link_quality_update(quality.link_quality);
        }
    }
}

void StatePlugin::m_add_status_frame(int id) // Called from main thread
{
    m_status_frames[id] = new CrazyflieStatusFrame(id, m_node, [this](const std::string& msg) {
        this->console_println(msg);
    });
    CrazyflieStatusWidget *widget = m_status_frames[id]->get_widget();
    m_status_frames[id]->setSizeHint(QSize(500, widget->getHeight()));

    m_ui.list_widget->addItem(m_status_frames[id]);
    m_ui.list_widget->setItemWidget(m_status_frames[id], widget);
    m_ui.list_widget->sortItems();
}

void StatePlugin::shutdownPlugin()
{
}

void 
StatePlugin::m_on_update_timer()
{


}

void StatePlugin::console_println(const std::string& msg)
{
    emit m_console_println(QString::fromStdString(msg));
}

void StatePlugin::m_on_console_println(const QString &msg)
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
    // Save the state of the UI elements
}

void StatePlugin::restoreSettings(
    const qt_gui_cpp::Settings & plugin_settings,
    const qt_gui_cpp::Settings & instance_settings)
{
    // Restore the state of the UI elements
}


} // namespace rqt_crazyflies



PLUGINLIB_EXPORT_CLASS(rqt_crazyflies::StatePlugin, rqt_gui_cpp::Plugin)