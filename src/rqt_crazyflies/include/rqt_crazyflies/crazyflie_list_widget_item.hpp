#pragma once
#include <QListWidgetItem>

namespace rqt_crazyflies
{

class CrazyflieListWidgetItem : public QListWidgetItem
{

public:
    CrazyflieListWidgetItem(int id)
    : QListWidgetItem()
    , m_id(id)
    {}
    ~CrazyflieListWidgetItem() {
    }

    bool operator<(const QListWidgetItem &other) const override
    {
        const CrazyflieListWidgetItem *otherItem = dynamic_cast<const CrazyflieListWidgetItem *>(&other);
        if (otherItem)
        {
            return m_id < otherItem->m_id;
        }
        return QListWidgetItem::operator<(other);
    }

private:
    int m_id;
};

} // namespace rqt_crazyflies