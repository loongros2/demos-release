// Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <chrono>
#include <string>

#include "quality_of_service_demo/common_nodes.hpp"

using namespace std::chrono_literals;

Talker::Talker(
  const std::string & topic_name,
  const rclcpp::QoS & qos_profile,
  const rclcpp::PublisherOptions & publisher_options,
  size_t publish_count,
  std::chrono::milliseconds assert_node_period,
  std::chrono::milliseconds assert_topic_period)
: Node("talker"),
  stop_at_count_(publish_count)
{
  RCLCPP_INFO(get_logger(), "Talker starting up");
  publisher_ = create_publisher<std_msgs::msg::String>(
    topic_name, qos_profile, publisher_options);
  publish_timer_ = create_wall_timer(500ms, std::bind(&Talker::publish, this));
  // If enabled, create timer to assert liveliness at the node level
  if (assert_node_period != 0ms) {
    assert_node_timer_ = create_wall_timer(
      assert_node_period,
      [this]() -> bool {
        return this->assert_liveliness();
      });
  }
  // If enabled, create timer to assert liveliness on the topic
  if (assert_topic_period != 0ms) {
    assert_topic_timer_ = create_wall_timer(
      assert_topic_period,
      [this]() -> bool {
        return publisher_->assert_liveliness();
      });
  }
}

void
Talker::pause_for(std::chrono::milliseconds pause_length)
{
  if (pause_timer_) {
    // Already paused - ignoring.
    return;
  }
  publish_timer_->cancel();
  pause_timer_ = create_wall_timer(
    pause_length,
    [this]() {
      // Publishing immediately on pause expiration and resuming regular interval.
      publish();
      publish_timer_->reset();
      pause_timer_ = nullptr;
    });
}

void
Talker::publish()
{
  std_msgs::msg::String msg;
  msg.data = "Talker says " + std::to_string(publish_count_);
  publish_count_ += 1;
  publisher_->publish(msg);
  if (stop_at_count_ > 0 && publish_count_ >= stop_at_count_) {
    publish_timer_->cancel();
  }
}

void
Talker::stop()
{
  if (assert_node_timer_) {
    assert_node_timer_->cancel();
    assert_node_timer_.reset();
  }
  if (assert_topic_timer_) {
    assert_topic_timer_->cancel();
    assert_topic_timer_.reset();
  }
  publish_timer_->cancel();
}

Listener::Listener(
  const std::string & topic_name,
  const rclcpp::QoS & qos_profile,
  const rclcpp::SubscriptionOptions & subscription_options,
  bool defer_subscribe)
: Node("listener"),
  qos_profile_(qos_profile),
  subscription_options_(subscription_options),
  topic_name_(topic_name)
{
  RCLCPP_INFO(get_logger(), "Listener starting up");
  if (!defer_subscribe) {
    start_listening();
  }
}

void
Listener::start_listening()
{
  if (!subscription_) {
    subscription_ = create_subscription<std_msgs::msg::String>(
      topic_name_,
      qos_profile_,
      [this](const typename std_msgs::msg::String::SharedPtr msg) -> void
      {
        RCLCPP_INFO(get_logger(), "Listener heard: [%s]", msg->data.c_str());
      },
      subscription_options_);
  }
}
