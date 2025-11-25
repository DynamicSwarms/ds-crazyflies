#include "rqt_crazyflies/crazyflie_connection.hpp"


namespace rqt_crazyflies
{

CrazyflieConnection::CrazyflieConnection(int cf_id, std::shared_ptr<rclcpp::Node> node)
: m_cf_id(cf_id)
{
    m_state_subscription = node->create_subscription<crazyflie_interfaces::msg::GenericLogData>(
        "/cf" + std::to_string(m_cf_id) + "/state",
        10,
        [this](const crazyflie_interfaces::msg::GenericLogData::SharedPtr msg) {
            if (this->m_state_update_callback) {
                this->m_state_update_callback(msg->values);
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

    m_takeoff_publisher = node->create_publisher<crazyflie_interfaces::msg::Takeoff>(
        "/cf" + std::to_string(m_cf_id) + "/takeoff", 10);
    m_land_publisher = node->create_publisher<crazyflie_interfaces::msg::Land>(
        "/cf" + std::to_string(m_cf_id) + "/land", 10);
    m_goto_publisher =  node->create_publisher<crazyflie_interfaces::msg::GoTo>(
        "/cf" + std::to_string(m_cf_id) + "/go_to", 10);
    m_set_parameters_client = node->create_client<rcl_interfaces::srv::SetParameters>(
        "/cf" + std::to_string(m_cf_id) + "/set_parameters");
}

CrazyflieConnection::~CrazyflieConnection()
{
    m_state_subscription.reset();
    m_console_subscription.reset();
    m_takeoff_publisher.reset();
    m_land_publisher.reset();
    m_goto_publisher.reset();
    m_set_parameters_client.reset();
}

void CrazyflieConnection::takeoff()
{
    auto msg = crazyflie_interfaces::msg::Takeoff();
    msg.height = 1.0;
    msg.duration.sec = 4;
    m_takeoff_publisher->publish(msg);
}

void CrazyflieConnection::land()
{
    auto msg = crazyflie_interfaces::msg::Land();
    msg.height = 0.0;
    msg.duration.sec = 4;
    m_land_publisher->publish(msg);
}

void CrazyflieConnection::goto_relative(const std::vector<double>& relative)
{
    auto msg = crazyflie_interfaces::msg::GoTo();
    msg.duration.sec = 2;
    msg.goal.x = relative[0];
    msg.goal.y = relative[1];
    msg.goal.z = relative[2];
    msg.relative = true;
    m_goto_publisher->publish(msg);
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