#pragma once


#include "rclcpp/rclcpp.hpp"

#include "crazyflie_interfaces/msg/generic_log_data.hpp"
#include <vector>


#include "rqt_crazyflies/crazyflie_connection.hpp"
#include <QListWidgetItem>

#include "rqt_crazyflies/crazyflie_status_widget.hpp"

namespace rqt_crazyflies
{

class CrazyflieStatusFrame : public QListWidgetItem
{

public:
    CrazyflieStatusFrame(int id, std::shared_ptr<rclcpp::Node> node, std::function<void(const std::string&)> console_printline);
    ~CrazyflieStatusFrame();
    void position_update(float x, float y, float z);
    void link_quality_update(float quality);
    CrazyflieStatusWidget *get_widget() const;

    bool operator<(const QListWidgetItem &other) const override;
private:
    void m_update_from_state(const std::shared_ptr<crazyflie_interfaces::msg::GenericLogData> msg);

    
private:
    int m_id;


    std::shared_ptr<rclcpp::Subscription<crazyflie_interfaces::msg::GenericLogData>> m_state_subscription;
    std::shared_ptr<CrazyflieConnection> m_cf_connection;   
};

} // namespace rqt_crazyflies