
#pragma once

#include <QDialog>
#include <QWidget>
#include <QTimer>

#include <rqt_crazyflies/crazyflie_connection.hpp>
#include "ui_crazyflie_control_modal.h"

namespace rqt_crazyflies
{
class CrazyflieControlModal : public QDialog
{
Q_OBJECT
public:
    CrazyflieControlModal(std::shared_ptr<rqt_crazyflies::CrazyflieConnection> connection);
    ~CrazyflieControlModal();

    void setPosition(float x, float y, float z);

private:
    void m_update_position();

private:
    std::shared_ptr<rqt_crazyflies::CrazyflieConnection> m_connection;

    float m_position[3] = {0.0f, 0.0f, 0.0f};

    QTimer* m_timer;
    Ui::CrazyflieControlModal m_ui; 
};

} // namespace rqt_crazyflies