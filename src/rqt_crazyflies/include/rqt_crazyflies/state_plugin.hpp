#pragma once

#include "ui_crazyflies_batteries_list.h"
#include "rclcpp/rclcpp.hpp"
#include "crazyflie_interfaces/msg/pose_stamped_array.hpp"
#include "crtp_interfaces/msg/crtp_link_qualities.hpp"
#include <rqt_gui_cpp/plugin.h> // With newer versions of ROS2 this must be .hpp

#include "rqt_crazyflies/crazyflie_status_frame.hpp"

#include <QWidget>  
#include <QTimer>

#include <unordered_map>
#include <deque>
namespace rqt_crazyflies
{

class StatePlugin : public rqt_gui_cpp::Plugin
{
    Q_OBJECT

public:
    StatePlugin();
    ~StatePlugin();

    virtual void initPlugin(qt_gui_cpp::PluginContext & context);

    virtual void shutdownPlugin();

    virtual void saveSettings(
        qt_gui_cpp::Settings & plugin_settings,
        qt_gui_cpp::Settings & instance_settings) const;
    virtual void restoreSettings(
        const qt_gui_cpp::Settings & plugin_settings,
        const qt_gui_cpp::Settings & instance_settings);
    
    void console_println(const std::string& msg);
private: 
    void m_on_update_timer();

    void m_on_positions_update(const crazyflie_interfaces::msg::PoseStampedArray::SharedPtr msg);
    void m_on_link_qualities_update(const crtp_interfaces::msg::CrtpLinkQualities::SharedPtr msg);

    void m_on_console_println(const QString &msg);
    void m_add_status_frame(int id);
protected: 
    Ui::CrazyfliesBatteriesList m_ui;
    QWidget *m_widget;

    QTimer *m_update_timer;


    std::shared_ptr<rclcpp::Node> m_node;
    std::shared_ptr<rclcpp::Subscription<crazyflie_interfaces::msg::PoseStampedArray>> m_pose_subscription;
    std::shared_ptr<rclcpp::Subscription<crtp_interfaces::msg::CrtpLinkQualities>> m_link_quality_subscription;
    

    std::unordered_map<int, CrazyflieStatusFrame*> m_status_frames;

    std::deque<QString> m_console_messages;

signals:
    void m_status_frame_add(int id);
    void m_console_println(const QString &msg);
};

} // namespace rqt_crazyflies
