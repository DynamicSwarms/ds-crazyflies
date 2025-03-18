/**
 * 2D Ellipse and Velocity Based collision avoidance algorithm.
*/

#include <cstdio>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/vector3.hpp"
#include "collision_avoidance_interfaces/srv/collision_avoidance.hpp"
#include <cmath>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <Eigen/Dense>

using std::placeholders::_1;
using std::placeholders::_2;



struct ObjectInfo {
    Eigen::Vector2d position;
    Eigen::Vector2d target;
    rclcpp::Time last_update;
};


class CollisionAvoidanceNode : public rclcpp::Node {
public: 
  CollisionAvoidanceNode() 
    : Node("collision_avoidance")
  {
    service = this->create_service<collision_avoidance_interfaces::srv::CollisionAvoidance>(
      "/collision_avoidance",
      std::bind(&CollisionAvoidanceNode::calculate_collisions, this, _1, _2)
    );

    cleanup_timer = this->create_wall_timer(
      std::chrono::milliseconds(200),
      std::bind(&CollisionAvoidanceNode::remove_old_objects, this)
    );

  } 
private: 
  rclcpp::Service<collision_avoidance_interfaces::srv::CollisionAvoidance>::SharedPtr service;
  rclcpp::TimerBase::SharedPtr cleanup_timer;
  std::unordered_map<uint8_t, ObjectInfo> active_objects;

private: 
  void remove_old_objects() {
    RCLCPP_INFO(this->get_logger(), "Count: %d", active_objects.size());
    rclcpp::Time current_time = this->now(); 
    rclcpp::Duration threshold(0, 200000000); // 0.2 seconds (200,000,000 nanoseconds)

    for (auto it = active_objects.begin(); it != active_objects.end(); ) {
          if (current_time - it->second.last_update > threshold) {
              // RCLCPP_INFO(this->get_logger(), "Removing object ID: %d", it->first);
              it = active_objects.erase(it);  // Remove object and get next iterator
          } else {
              ++it;  // Move to the next item
          }
      }
  }
  
  void calculate_collisions(
      const std::shared_ptr<collision_avoidance_interfaces::srv::CollisionAvoidance::Request> request,
      std::shared_ptr<collision_avoidance_interfaces::srv::CollisionAvoidance::Response> response) {


    uint8_t id = request->id;
    Eigen::Vector2d position(request->position.x,request->position.y);
    Eigen::Vector2d target(request->target.x,request->target.y);
    active_objects[id] = {position, target, this->now()};

    double min_distance = request->min_distance;
    double force_distance = request->force_distance;
    double strength = request->strength;

    
    // There are 3 targets taken into account. 

    // An urge due to our velocity based collision avoidance
    double urge_distance = 1;
    double urge_factor = 1;

    // A potential field target
    double potential_factor = 1;
    double potential_distance = 0.55;
    double potential_distance_min = potential_distance / 2.0;
    
    // And the original target
    double target_factor = 1;                             


    Eigen::Vector2d urges_sum(0.0,0.0);
    Eigen::Vector2d potentials_sum(0.0,0.0);
    bool collision = false;

    Eigen::Vector2d velocity = target - position;  
    double v1_len = velocity.norm();
  
    // We are called 1, the other one is called 2
    // Positions: position, other_position
    // Velocities: velocity, other_velocity
    // Targets: target, other_target    
    if (active_objects.size() < 2) {
      response->target = request->target;
      response->collision = false;
      return;
    } else {
      for(const auto& [other_id, other_data] : active_objects) {
        if (other_id == id) continue;
        Eigen::Vector2d other_position(other_data.position);
        Eigen::Vector2d other_target(other_data.target);
        Eigen::Vector2d other_velocity = other_target - other_position;
        double v2_len = other_velocity.norm();

        Eigen::Vector2d p12 = position - other_position;
        Eigen::Vector2d p21 = other_position - position;
        double distance = p12.norm(); // The distance between both objects

        // First check if we are close enough a computation is worth
        if (distance < urge_distance * 1.125) 
        {
          // Ellipse around the direction Vector of v1 (ellipse1_p1 is the position of 1)
          Eigen::Vector2d ellipse1_p2 = position + urge_distance * velocity.normalized();
          // Ellipse around the direction vector of v2
          Eigen::Vector2d ellipse2_p2 = other_position + urge_distance * other_velocity.normalized();

          bool p1_inside_e2 = inside_ellipse(position, other_position, ellipse2_p2, urge_distance * 1.25);
          bool p2_inside_e1 = inside_ellipse(other_position, position, ellipse1_p2, urge_distance * 1.25);

          if (!p2_inside_e1 && !p1_inside_e2) {} // No collision, do nothing.
          else if (v1_len > 0.3 && v2_len > 0.3) { // Both are moving.
            // Check if we move in opposite or similar direction
            if (velocity.dot(other_velocity) < 0.0) { // Opposite direction
              if (p12.dot(other_velocity) < 0) {} // We have already passed (Only potential field gets applied)
              else { // Heading towards one another, but did not yet pass
                // We need to decide if we strave left or right
                Eigen::Vector2d velocity_rotated = rotate_90ccw(velocity);
                Eigen::Vector2d other_velocity_rotated = rotate_90ccw(other_velocity);
                int p1 = - signum(p21.dot(velocity_rotated));
                int p2 = - signum(p12.dot(other_velocity_rotated));
                
                // E.g. if velocity vectors cross p1 != p2 -> Need a vote
                int p = v1_len < v2_len ? p1 : p2; // Slower object gets the vote (arbitrary) but it needs to be same for both.
                urges_sum += velocity_rotated * p;
              }
            } // The else case is both are moving in same direction, which is fine.
          } else if (v1_len >= 0.3) { // p2 stationary
            if (p2_inside_e1) {
              double val = p21.dot(velocity) / (distance * v1_len);
              if (val > 0) {  // We are heading towards c2
                Eigen::Vector2d velocity_rotated = rotate_90ccw(velocity);
                double p = - signum(p21.dot(velocity_rotated));
                urges_sum += velocity_rotated * p * (1  - val);
              }
            }
          } else if (v2_len >= 0.3) { // p1 stationary
            if (p1_inside_e2) {
              double val = p12.dot(other_velocity) / (distance * v2_len);
              if (val > 0) {  // We are heading towards c1
                Eigen::Vector2d other_velocity_rotated = rotate_90ccw(other_velocity);
                double p = - signum(p12.dot(other_velocity_rotated));
                urges_sum +=  - other_velocity_rotated * p * (1  - val);  
              }
            }
          }

        }

        if (distance < potential_distance) {
          // map distance to value in range [1, 0] -> how dangerously close are we
          double clamped_d = std::max(potential_distance_min, distance);  // Ensure d is at least potential_distance_min
          double mapped_value = map(clamped_d, potential_distance_min, potential_distance, 1.0, 0.0);
          double fi = std::pow(mapped_value, 1.0);
          potentials_sum += p12 * fi;
        }

        if (distance < min_distance) {} // TODO Do smart stuff if we are super close

        if (distance < potential_distance || distance < urge_distance) collision = true;
      } // Iteration over all others
      
      double length = collision ? std::max(0.1, v1_len) : v1_len; // We need to move if there is a collision, even if we would like to stand still.

      Eigen::Vector2d relative_target_unit = velocity.normalized();
      Eigen::Vector2d urge_unit = urges_sum.normalized();
      Eigen::Vector2d potential_unit = potentials_sum.normalized();

      Eigen::Vector2d combined = urge_unit * urge_factor + potential_unit * potential_factor + relative_target_unit * target_factor;
      
      Eigen::Vector2d new_target = position + combined.normalized() * length;


      response->target.x = new_target.x();
      response->target.y = new_target.y();
      response->target.z = request->target.z;
      response->collision = collision;
      return;
    }
  }


private: 
  // If your number X falls between A and B, and you would like Y to fall between C and D
  double map(double x, double a, double b, double c, double d) 
  {
    return (x - a) / (b - a) * (d - c) + c;
  }
  
  // The signum is -1 if negative, 1 if positive, 0 if 0
  int signum(double d)
  {
    return (0.0 < d) - (d < 0.0);
  }

  // Rotate a vector 90 degrees counter clock wise
  Eigen::Vector2d rotate_90ccw(const Eigen::Vector2d& v) 
  {
    return Eigen::Vector2d(-v.y(), v.x());
  }

  /**
   * Checks whether a point p_check is inside the ellipse defined by p1, p2 and r
   * @param p_check: point to check
   * @param p1: first point of the ellipse
   * @param p2: second point of the ellipse
   * @param r: radius of the ellipse
   * @return bool: true if p_check is inside ellipse
  */
  bool inside_ellipse(const Eigen::Vector2d& p_check,const Eigen::Vector2d& p1, const Eigen::Vector2d& p2, double r) {
    double d1 = (p_check - p1).norm();
    double d2 = (p_check - p2).norm();
    return d1 + d2 < r;
  }

};


int main(int argc, char ** argv)
{
  (void) argc;
  (void) argv;
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CollisionAvoidanceNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();

  return 0;
}
