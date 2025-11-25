#pragma once

#include "crazyflie_interfaces/msg/takeoff.hpp"
#include "crazyflie_interfaces/msg/land.hpp"
#include "crazyflie_interfaces/msg/go_to.hpp"

#include "crazyflie_interfaces/msg/generic_log_data.hpp"

#include "rcl_interfaces/srv/set_parameters.hpp"
#include "std_msgs/msg/string.hpp"
#include "rclcpp/rclcpp.hpp"

#include <vector>

namespace rqt_crazyflies
{
class CrazyflieConnection
{
public:
    CrazyflieConnection(int cf_id, std::shared_ptr<rclcpp::Node> node);
    ~CrazyflieConnection();

    void takeoff();
    void land();
    void goto_relative(const std::vector<double>& relative);

    void set_parameters(const std::vector<rclcpp::Parameter>& parameters);

    int get_id() const;

    void set_state_update_callback(std::function<void(const std::vector<double>&)> callback);
    void clear_state_update_callback();

    void set_position_update_callback(std::function<void(const std::vector<double>&)> callback);
    void clear_position_update_callback();

    void set_console_update_callback(std::function<void(const std::string&)> callback);
    void clear_console_update_callback();

    void set_link_quality_update_callback(std::function<void(float)> callback);
    void clear_link_quality_update_callback();

    void set_position(const std::vector<double>& position);
    void set_link_quality(float quality);

private:
    std::function<void(const std::vector<double>&)> m_state_update_callback = nullptr;
    std::function<void(const std::vector<double>&)> m_position_update_callback = nullptr;
    std::function<void(const std::string&)> m_console_update_callback = nullptr;
    std::function<void(float)> m_link_quality_update_callback = nullptr;

    int m_cf_id;
    std::shared_ptr<rclcpp::Subscription<crazyflie_interfaces::msg::GenericLogData>> m_state_subscription;
    std::shared_ptr<rclcpp::Subscription<std_msgs::msg::String>> m_console_subscription;
    std::shared_ptr<rclcpp::Publisher<crazyflie_interfaces::msg::Takeoff>> m_takeoff_publisher;
    std::shared_ptr<rclcpp::Publisher<crazyflie_interfaces::msg::Land>> m_land_publisher;
    std::shared_ptr<rclcpp::Publisher<crazyflie_interfaces::msg::GoTo>> m_goto_publisher;
    std::shared_ptr<rclcpp::Client<rcl_interfaces::srv::SetParameters>> m_set_parameters_client;
};

} // namespace rqt_crazyflies