#!/usr/bin/python3

import carla

import rospy
from geometry_msgs.msg import TransformStamped
from carla_player_publisher_msg.msg import TransformStampedArray

class CarlaPlayerPublisher:
    def __init__(self):
        self.pub_obj = rospy.Publisher("~object", TransformStampedArray, queue_size=1)
        self.pub_local_obj = rospy.Publisher("~local_object", TransformStampedArray, queue_size=1)
        try:
            self.client = carla.Client('127.0.0.1', 2000)
            self.client.set_timeout(2000.0)
        finally:
            print("")

    def get_data(self):
        actor_list = self.client.get_world().get_actors()
        if actor_list.filter('*erp42*'):
            obj_list = []
            obj_local_list = []
            for actor in actor_list.filter('*erp42'):                
                obj_list.append(self.Carla2Geometry(actor))
                obj_list[len(obj_list) - 1].header.frame_id = "ego_vehicle"
            for actor in actor_list.filter('*npc*'):                
                obj_list.append(self.Carla2Geometry(actor))
                obj_local_list.append(self.LocalObjSet(obj_list[0], obj_list[len(obj_list) - 1]))
            self.pub_obj.publish(obj_list)
            self.pub_local_obj.publish(obj_local_list)

    def Carla2Geometry(self, actor):
        obj_data = TransformStamped()
        obj_data.header.frame_id = str(actor.id)
        obj_data.header.stamp = rospy.Time.now()
        obj_data.child_frame_id = "map"
        transform = actor.get_transform()
        obj_data.transform.translation.x = transform.location.x
        obj_data.transform.translation.y = transform.location.y
        obj_data.transform.translation.z = transform.location.z
        obj_data.transform.rotation.x = transform.rotation.roll
        obj_data.transform.rotation.y = transform.rotation.pitch
        obj_data.transform.rotation.z = transform.rotation.yaw
        return obj_data
    
    def LocalObjSet(self, ego, obj):
        obj_data = TransformStamped()
        obj_data.header = obj.header
        obj_data.child_frame_id = "ego_vehicle"
        obj_data.transform.translation.x = ego.transform.translation.x - obj.transform.translation.x
        obj_data.transform.translation.y = ego.transform.translation.y - obj.transform.translation.y
        obj_data.transform.translation.z = ego.transform.translation.z - obj.transform.translation.z
        obj_data.transform.rotation.x = ego.transform.rotation.x - obj.transform.rotation.x
        obj_data.transform.rotation.y = ego.transform.rotation.y - obj.transform.rotation.y
        obj_data.transform.rotation.z = ego.transform.rotation.z - obj.transform.rotation.z
        return obj_data

def main():
    rospy.init_node("carla_player_publisher", anonymous=True)
    CPP = CarlaPlayerPublisher()
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        CPP.get_data()
        rate.sleep()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
