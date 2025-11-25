#include "rqt_crazyflies/crazyflie_status_frame.hpp"
#include <QObject>
namespace rqt_crazyflies
{

CrazyflieStatusFrame::CrazyflieStatusFrame(int id, std::shared_ptr<rclcpp::Node> node, std::function<void(const std::string&)> console_printline)
: QListWidgetItem()
, m_id(id)
{
    m_cf_connection = std::make_shared<CrazyflieConnection>(m_id, node);
    m_cf_connection->set_console_update_callback(console_printline);
}

CrazyflieStatusFrame::~CrazyflieStatusFrame()
{
    m_cf_connection->clear_console_update_callback();
}

void 
CrazyflieStatusFrame::position_update(float x, float y, float z)
{
  m_cf_connection->set_position({x, y, z});
}

void 
CrazyflieStatusFrame::link_quality_update(float quality)
{
    m_cf_connection->set_link_quality(quality);
}

CrazyflieStatusWidget * CrazyflieStatusFrame::get_widget() const
{
    return new CrazyflieStatusWidget(nullptr, m_cf_connection);
}

bool 
CrazyflieStatusFrame::operator<(const QListWidgetItem &other) const
{
    const CrazyflieStatusFrame *otherFrame = dynamic_cast<const CrazyflieStatusFrame *>(&other);
    if (otherFrame)
    {
        return m_id < otherFrame->m_id;
    }
    return QListWidgetItem::operator<(other);
}




} // namespace rqt_crazyflies