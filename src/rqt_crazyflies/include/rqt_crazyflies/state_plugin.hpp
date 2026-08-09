#pragma once

#include "ui_crazyflies_batteries_list.h"
#include "rclcpp/rclcpp.hpp"
#include "crazyflie_interfaces/msg/pose_named_array.hpp"
#ifdef RQT_CRAZYFLIES_HAS_CRTP
#include "crtp_interfaces/msg/crtp_link_qualities.hpp"
#endif
#include <rqt_gui_cpp/plugin.hpp> // With newer versions of ROS2 this must be .hpp

#include "rqt_crazyflies/crazyflie_list_widget_item.hpp"
#include "rqt_crazyflies/crazyflie_status_widget.hpp"
#include "rqt_crazyflies/crazyflie_connection.hpp"

#include <QWidget>  
#include <QTimer>

#include <unordered_map>
#include <deque>
namespace rqt_crazyflies
{

struct CrazyflieListEntry
{
    CrazyflieListWidgetItem* item;
    CrazyflieStatusWidget* widget;
    std::shared_ptr<CrazyflieConnection> connection;
};

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

    void m_on_positions_update(const crazyflie_interfaces::msg::PoseNamedArray::SharedPtr msg);
#ifdef RQT_CRAZYFLIES_HAS_CRTP
    void m_on_link_qualities_update(const crtp_interfaces::msg::CrtpLinkQualities::SharedPtr msg);
#endif


    void m_signal_handler_console_println(const QString &msg);
    void m_signal_handler_add_crazyflie(int id);
    
protected: 
    Ui::CrazyfliesBatteriesList m_ui;
    QWidget *m_widget;

    std::shared_ptr<rclcpp::Node> m_node;
    std::shared_ptr<rclcpp::Subscription<crazyflie_interfaces::msg::PoseNamedArray>> m_pose_subscription;
#ifdef RQT_CRAZYFLIES_HAS_CRTP
    std::shared_ptr<rclcpp::Subscription<crtp_interfaces::msg::CrtpLinkQualities>> m_link_quality_subscription;
#endif
    

    std::unordered_map<int, CrazyflieListEntry> m_crazyflies;

    std::deque<QString> m_console_messages;

signals:
    void console_println_signal(const QString &msg);
    void add_crazyflie_signal(int id);
};

} // namespace rqt_crazyflies
