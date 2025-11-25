#pragma once

#include "ui_crazyflie_status_widget.h"
#include "rqt_crazyflies/crazyflie_connection.hpp"

namespace rqt_crazyflies
{

class CrazyflieStatusWidget : public QWidget
{
    Q_OBJECT

public:
    CrazyflieStatusWidget(QWidget *parent = nullptr, std::shared_ptr<CrazyflieConnection> cf_connection = nullptr);
    ~CrazyflieStatusWidget();

    int getHeight() const;

public:
    void update_state(std::vector<double> state);
    void update_position(float x, float y, float z);
    void update_link_quality(float quality);

private:
    void m_check_position_update_timer_callback();

    void m_on_link_quality_updated(float quality);
    void m_on_position_updated();
    void m_on_state_updated();


private:
    Ui::CrazyflieStatusWidget m_ui;
    std::shared_ptr<CrazyflieConnection> m_cf_connection;

    enum class ChargeState {
        BATTERY, 
        CHARGING, 
        CHARGED, 
        LOWPOWER, 
        SHUTDOWN
    };

    static const char* charge_state_to_string(ChargeState state) {
        switch (state) {
            case ChargeState::BATTERY:   return "BATTERY";
            case ChargeState::CHARGING:  return "CHARGING";
            case ChargeState::CHARGED:   return "CHARGED";
            case ChargeState::LOWPOWER:  return "LOWPOWER";
            case ChargeState::SHUTDOWN:  return "SHUTDOWN";
            default:                     return "UNKNOWN";
        }
    }

    float m_voltage = 0.0; 
    float m_current = 0.0;
    ChargeState m_charge_state = ChargeState::BATTERY; 
    bool m_canFly = false;
    bool m_isFlying = false;
    bool m_isTumbled = false;

    float m_position[3] = {0.0f, 0.0f, 0.0f}; // x, y, z

    std::chrono::steady_clock::time_point m_last_position_update = std::chrono::steady_clock::now();
    QTimer* m_check_position_update_timer;

signals:
    void m_position_updated();
    void m_state_updated();
    void m_link_quality_updated(float);

};
} // namespace rqt_crazyflies