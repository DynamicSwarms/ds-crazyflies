#include "rqt_crazyflies/crazyflie_status_widget.hpp"
#include "rqt_crazyflies/crazyflie_control_modal.hpp"
#include "rclcpp/rclcpp.hpp"
namespace rqt_crazyflies
{

CrazyflieStatusWidget::CrazyflieStatusWidget(QWidget *parent, std::shared_ptr<CrazyflieConnection> cf_connection)
: QWidget(parent)
, m_cf_connection(cf_connection)
{
    m_ui.setupUi(this);

    m_ui.label_id->setText(QString("ID: %1 (0x%2)").arg(m_cf_connection->get_id()).arg(m_cf_connection->get_id(), 0, 16).toUpper());

    connect(m_ui.flight_control_modal, &QPushButton::clicked, this, [this]() {
        CrazyflieControlModal modal(m_cf_connection);
        this->connect(this, &CrazyflieStatusWidget::m_position_updated, &modal, [this, &modal]() {
            modal.setPosition(m_position[0], m_position[1], m_position[2]);
        });
        modal.exec();
    });

    connect(this, &CrazyflieStatusWidget::m_position_updated, this, &CrazyflieStatusWidget::m_on_position_updated);
    connect(this, &CrazyflieStatusWidget::m_state_updated, this, &CrazyflieStatusWidget::m_on_state_updated);
    connect(this, &CrazyflieStatusWidget::m_link_quality_updated, this, &CrazyflieStatusWidget::m_on_link_quality_updated);

    connect(m_ui.propeller_test_button, &QPushButton::clicked, this, [this]() {
        m_cf_connection->set_parameters({rclcpp::Parameter("health.startPropTest", 1)});
    });
    connect(m_ui.battery_test_button, &QPushButton::clicked, this, [this]() {
        m_cf_connection->set_parameters({rclcpp::Parameter("health.startBatTest", 1)});
    });


    
    m_cf_connection->set_state_update_callback([this](const std::vector<double>& state) {
        this->update_state(state);
    });
    m_cf_connection->set_position_update_callback([this](const std::vector<double>& position) {
        this->update_position(position[0], position[1], position[2]);
    });
    m_cf_connection->set_link_quality_update_callback([this](float quality) {
        this->update_link_quality(quality);
    });

    m_check_position_update_timer = new QTimer(this);
    connect(m_check_position_update_timer, &QTimer::timeout, this, &CrazyflieStatusWidget::m_check_position_update_timer_callback);
    m_check_position_update_timer->start(200);

}

CrazyflieStatusWidget::~CrazyflieStatusWidget()
{
    m_cf_connection->clear_state_update_callback();
    m_cf_connection->clear_position_update_callback();
}

int
CrazyflieStatusWidget::getHeight() const
{
    return m_ui.battery_progress->height() * 1.1;
}

void 
CrazyflieStatusWidget::update_position(float x, float y, float z)
{
    this->setEnabled(true);
    m_last_position_update = std::chrono::steady_clock::now();
    m_position[0] = x;
    m_position[1] = y;
    m_position[2] = z;
    emit m_position_updated();;
}

void 
CrazyflieStatusWidget::update_link_quality(float quality)
{
    emit m_link_quality_updated(quality);
}

void 
CrazyflieStatusWidget::m_check_position_update_timer_callback()
{
    auto now = std::chrono::steady_clock::now();
    std::chrono::duration<double> elapsed = now - m_last_position_update;
    if (elapsed.count() > 0.25)
    {
        this->setEnabled(false);
    }
}

void 
CrazyflieStatusWidget::m_on_position_updated()
{
    m_ui.flight_control_modal->setToolTip(QString("Position: (%1, %2, %3)")
        .arg(m_position[0], 0, 'f', 2)
        .arg(m_position[1], 0, 'f', 2)
        .arg(m_position[2], 0, 'f', 2));
}

void
CrazyflieStatusWidget::m_on_link_quality_updated(float quality)
{
    m_ui.link_quality_progress->setValue(static_cast<int>(quality * 100.0f));
}

void 
CrazyflieStatusWidget::update_state(std::vector<double> state)
{
    if (state.size() >= 6)
    {
        m_voltage = state[0];
        m_current = state[1];
        m_charge_state = ChargeState(int(state[2]));
        m_canFly = bool(int(state[3]));
        m_isFlying = bool(int(state[4]));
        m_isTumbled = bool(int(state[5]));
        emit m_state_updated();
    }
    if (state.size() == 1) // Webots update
    {
        m_voltage = state[0];
        emit m_state_updated();
    }
}

void 
CrazyflieStatusWidget::m_on_state_updated()
{
    m_ui.battery_progress->setValue(
        static_cast<int>(
            std::max(0.0, std::min(100.0, (m_voltage / 4.2) * 100.0))
        )
    );
    m_ui.battery_label->setText(QString::number(m_voltage, 'f', 2) + " V");
    m_ui.charge_label->setText(QString::number(m_current, 'f', 2) + " mA");
    m_ui.state_label->setText(charge_state_to_string(m_charge_state));
    m_ui.canFly_icon->setText(m_canFly ? "🟢" : "🔴");
    m_ui.isFlying_icon->setText(m_isFlying ? "🛫" : "🏠");
    m_ui.isTumbled_icon->setText(m_isTumbled ? "💥" : "🟢");

}

}// namespace rqt_crazyflies