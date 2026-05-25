#include "rqt_crazyflies/crazyflie_connection.hpp"


namespace rqt_crazyflies
{

CrazyflieConnection::CrazyflieConnection(
    int cf_id, 
    std::shared_ptr<rclcpp::node_interfaces::NodeBaseInterface> node_base_interface, 
    std::shared_ptr<rclcpp::node_interfaces::NodeTopicsInterface> node_topics_interface, 
    std::shared_ptr<rclcpp::node_interfaces::NodeGraphInterface> node_graph_interface,
    std::shared_ptr<rclcpp::node_interfaces::NodeServicesInterface> node_services_interface
)
: m_cf_id(cf_id)
{
    m_state_subscription = rclcpp::create_subscription<crazyflie_interfaces::msg::LogDataGeneric>(
        node_topics_interface,
        "/cf" + std::to_string(m_cf_id) + "/state",
        10,
        [this](const crazyflie_interfaces::msg::LogDataGeneric::SharedPtr msg) {
            if (this->m_state_update_callback) {
                std::vector<double> values_double(msg->values.begin(), msg->values.end());
                this->m_state_update_callback(values_double);
            }
        }
    );

    m_console_subscription = rclcpp::create_subscription<std_msgs::msg::String>(
        node_topics_interface,
        "/cf" + std::to_string(m_cf_id) + "/console",
        10,
        [this](const std_msgs::msg::String::SharedPtr msg) {
            if (this->m_console_update_callback) {
                std::stringstream ss;
                ss << "[0x" << std::hex << m_cf_id << "] " << msg->data;
                this->m_console_update_callback(ss.str());
            }
        }
    );

    m_takeoff_client = rclcpp::create_client<crazyflie_interfaces::srv::Takeoff>(
        node_base_interface,
        node_graph_interface,
        node_services_interface,
        "/cf" + std::to_string(m_cf_id) + "/takeoff");
    m_land_client = rclcpp::create_client<crazyflie_interfaces::srv::Land>(
        node_base_interface,
        node_graph_interface,
        node_services_interface,
        "/cf" + std::to_string(m_cf_id) + "/land");
    m_goto_client = rclcpp::create_client<crazyflie_interfaces::srv::GoTo>(
        node_base_interface,
        node_graph_interface,
        node_services_interface,
        "/cf" + std::to_string(m_cf_id) + "/go_to");
    m_set_parameters_client = rclcpp::create_client<rcl_interfaces::srv::SetParameters>(
        node_base_interface,
        node_graph_interface,
        node_services_interface,
        "/cf" + std::to_string(m_cf_id) + "/set_parameters");
}

CrazyflieConnection::~CrazyflieConnection()
{
    m_state_subscription.reset();
    m_console_subscription.reset();
    m_takeoff_client.reset();
    m_land_client.reset();
    m_goto_client.reset();
    m_set_parameters_client.reset();
}

void CrazyflieConnection::takeoff()
{
    auto request = std::make_shared<crazyflie_interfaces::srv::Takeoff::Request>();
    request->height = 1.0;
    request->duration.sec = 4;

    m_takeoff_client->async_send_request(request);
}

void CrazyflieConnection::land()
{
    auto request = std::make_shared<crazyflie_interfaces::srv::Land::Request>();
    request->height = 0.0;
    request->duration.sec = 4;
    m_land_client->async_send_request(request);
}

void CrazyflieConnection::goto_target(
    const std::vector<double>& target,
    float yaw_rad, 
    bool relative_flag)
{
    auto request = std::make_shared<crazyflie_interfaces::srv::GoTo::Request>();
    request->duration.sec = 2;
    request->goal.x = target[0];
    request->goal.y = target[1];
    request->goal.z = target[2];
    request->yaw = yaw_rad;
    request->relative = relative_flag;

    m_goto_client->async_send_request(request);
}

void CrazyflieConnection::set_parameters(const std::vector<rclcpp::Parameter>& parameters)
{
    auto request = std::make_shared<rcl_interfaces::srv::SetParameters::Request>();
    for (const auto& param : parameters) {
        request->parameters.push_back(param.to_parameter_msg());
    }
    m_set_parameters_client->async_send_request(request);
}

void CrazyflieConnection::set_state_update_callback(std::function<void(const std::vector<double>&)> callback)
{
    m_state_update_callback = callback;
}

void CrazyflieConnection::clear_state_update_callback()
{
    m_state_update_callback = nullptr;
}

void CrazyflieConnection::set_position_update_callback(std::function<void(const std::vector<double>&)> callback)
{
    m_position_update_callback = callback;
}

void CrazyflieConnection::clear_position_update_callback()
{
    m_position_update_callback = nullptr;
}

void CrazyflieConnection::set_console_update_callback(std::function<void(const std::string&)> callback)
{
    m_console_update_callback = callback;
}

void CrazyflieConnection::clear_console_update_callback()
{
    m_console_update_callback = nullptr;
}

void CrazyflieConnection::set_link_quality_update_callback(std::function<void(float)> callback)
{
    m_link_quality_update_callback = callback;
}

void CrazyflieConnection::clear_link_quality_update_callback()
{
    m_link_quality_update_callback = nullptr;
}

int CrazyflieConnection::get_id() const
{
    return m_cf_id;
}

void CrazyflieConnection::set_position(const std::vector<double>& position)
{
    m_position = position;
    if (m_position_update_callback) {
        m_position_update_callback(position);
    }
}

void CrazyflieConnection::set_link_quality(float quality)
{
    m_link_quality = quality;
    if (m_link_quality_update_callback) {
        m_link_quality_update_callback(quality);
    }
}

} // namespace rqt_crazyflies