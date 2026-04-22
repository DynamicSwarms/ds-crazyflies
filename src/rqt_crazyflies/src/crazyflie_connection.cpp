#include "rqt_crazyflies/crazyflie_connection.hpp"


namespace rqt_crazyflies
{

CrazyflieConnection::CrazyflieConnection(int cf_id, std::shared_ptr<rclcpp::Node> node)
: m_cf_id(cf_id)
{
    m_state_subscription = node->create_subscription<crazyflie_interfaces::msg::LogDataGeneric>(
        "/cf" + std::to_string(m_cf_id) + "/state",
        10,
        [this](const crazyflie_interfaces::msg::LogDataGeneric::SharedPtr msg) {
            if (this->m_state_update_callback) {
                std::vector<double> values_double(msg->values.begin(), msg->values.end());
                this->m_state_update_callback(values_double);
            }
        }
    );

    m_console_subscription = node->create_subscription<std_msgs::msg::String>(
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

    m_takeoff_client = node->create_client<crazyflie_interfaces::srv::Takeoff>(
        "/cf" + std::to_string(m_cf_id) + "/takeoff");
    m_land_client = node->create_client<crazyflie_interfaces::srv::Land>(
        "/cf" + std::to_string(m_cf_id) + "/land");
    m_goto_client = node->create_client<crazyflie_interfaces::srv::GoTo>(
        "/cf" + std::to_string(m_cf_id) + "/go_to");
    m_set_parameters_client = node->create_client<rcl_interfaces::srv::SetParameters>(
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

void CrazyflieConnection::goto_relative(const std::vector<double>& relative)
{
    auto request = std::make_shared<crazyflie_interfaces::srv::GoTo::Request>();
    request->duration.sec = 2;
    request->goal.x = relative[0];
    request->goal.y = relative[1];
    request->goal.z = relative[2];
    request->relative = true;
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
    if (m_position_update_callback) {
        m_position_update_callback(position);
    }
}

void CrazyflieConnection::set_link_quality(float quality)
{
    if (m_link_quality_update_callback) {
        m_link_quality_update_callback(quality);
    }
}

} // namespace rqt_crazyflies