#include "rqt_crazyflies/crazyflie_control_modal.hpp"
namespace rqt_crazyflies
{

CrazyflieControlModal::CrazyflieControlModal(std::shared_ptr<rqt_crazyflies::CrazyflieConnection> connection)
: m_connection(connection)
{
    m_ui.setupUi(this);

    setWindowTitle(QString("Crazyflie Control 0x%1").arg(QString::number(m_connection->get_id(), 16).toUpper()));

    m_timer = new QTimer(this);
    connect(m_timer, &QTimer::timeout, this, &CrazyflieControlModal::m_update_position);
    m_timer->start(100);

    connect(m_ui.land_button, &QPushButton::clicked, this, [this]() { m_connection->land(); });
    connect(m_ui.takeoff_button, &QPushButton::clicked, this, [this]() { m_connection->takeoff(); });
    connect(m_ui.forward_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({0.5, 0.0, 0.0}); });
    connect(m_ui.backward_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({-0.5, 0.0, 0.0}); });
    connect(m_ui.left_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({0.0, 0.5, 0.0}); });
    connect(m_ui.right_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({0.0, -0.5, 0.0}); });
    connect(m_ui.up_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({0.0, 0.0, 0.5}); });
    connect(m_ui.down_button, &QPushButton::clicked, this, [this]() { m_connection->goto_relative({0.0, 0.0, -0.5}); });
}

CrazyflieControlModal::~CrazyflieControlModal()
{
}

void CrazyflieControlModal::setPosition(float x, float y, float z)
{
    m_position[0] = x;
    m_position[1] = y;
    m_position[2] = z;
}

void CrazyflieControlModal::m_update_position()
{
    m_ui.position_label->setText(QString("Position: (%1, %2, %3)")
        .arg(m_position[0], 0, 'f', 2)
        .arg(m_position[1], 0, 'f', 2)
        .arg(m_position[2], 0, 'f', 2));
}

} // namespace rqt_crazyflies