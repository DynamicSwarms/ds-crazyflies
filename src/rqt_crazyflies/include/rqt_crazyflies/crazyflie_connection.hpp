#pragma once

#include "crazyflie_interfaces/srv/takeoff.hpp"
#include "crazyflie_interfaces/srv/land.hpp"
#include "crazyflie_interfaces/srv/go_to.hpp"

#include "crazyflie_interfaces/msg/log_data_generic.hpp"

#include "rcl_interfaces/srv/set_parameters.hpp"
#include "std_msgs/msg/string.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_srvs/srv/trigger.hpp"
#include "rclcpp/rclcpp.hpp"

#include <vector>
#include <algorithm>

namespace rqt_crazyflies
{
class CrazyflieConnection
{
public:
    CrazyflieConnection(
        int cf_id,     
        std::shared_ptr<rclcpp::node_interfaces::NodeBaseInterface> node, 
        std::shared_ptr<rclcpp::node_interfaces::NodeTopicsInterface> node_topics_interface, 
        std::shared_ptr<rclcpp::node_interfaces::NodeGraphInterface> node_graph_interface,
        std::shared_ptr<rclcpp::node_interfaces::NodeServicesInterface> node_services_interface);
    ~CrazyflieConnection();

    void takeoff();
    void land();
    void goto_target(
        const std::vector<double>& target,
        float yaw_rad = 0.0, 
        bool relative = true);

    void set_parameters(const std::vector<rclcpp::Parameter>& parameters);
    void simulate_crash();
    void set_simulated_battery(float voltage);
    bool can_simulate_crash();
    bool can_set_simulated_battery();

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
    std::vector<double> m_position;
    float m_link_quality;

    std::function<void(const std::vector<double>&)> m_state_update_callback = nullptr;
    std::function<void(const std::vector<double>&)> m_position_update_callback = nullptr;
    std::function<void(const std::string&)> m_console_update_callback = nullptr;
    std::function<void(float)> m_link_quality_update_callback = nullptr;

    int m_cf_id;
    std::shared_ptr<rclcpp::node_interfaces::NodeBaseInterface> m_node_base_interface;
    std::shared_ptr<rclcpp::node_interfaces::NodeTopicsInterface> m_node_topics_interface;
    std::shared_ptr<rclcpp::node_interfaces::NodeGraphInterface> m_node_graph_interface;
    std::shared_ptr<rclcpp::node_interfaces::NodeServicesInterface> m_node_services_interface;
    std::shared_ptr<rclcpp::Subscription<crazyflie_interfaces::msg::LogDataGeneric>> m_state_subscription;
    std::shared_ptr<rclcpp::Subscription<std_msgs::msg::String>> m_console_subscription;
    std::shared_ptr<rclcpp::Client<crazyflie_interfaces::srv::Takeoff>> m_takeoff_client;
    std::shared_ptr<rclcpp::Client<crazyflie_interfaces::srv::Land>> m_land_client;
    std::shared_ptr<rclcpp::Client<crazyflie_interfaces::srv::GoTo>> m_goto_client;
    std::shared_ptr<rclcpp::Client<rcl_interfaces::srv::SetParameters>> m_set_parameters_client;
    std::shared_ptr<rclcpp::Client<std_srvs::srv::Trigger>> m_simulate_crash_client;
    std::shared_ptr<rclcpp::Publisher<std_msgs::msg::Float32>> m_simulated_battery_publisher;
};

} // namespace rqt_crazyflies
