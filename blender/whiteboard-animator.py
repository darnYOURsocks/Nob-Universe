"""
Blender Whiteboard Animator
Animate whiteboard drawings and conceptual diagrams
Author: ŊOB Universe
"""

import bpy
import bmesh
from mathutils import Vector, Matrix
import random

class WhiteboardAnimator:
    """Animate 2D drawings on a whiteboard plane"""
    
    def __init__(self):
        self.drawing_objects = []
        self.frame_start = 1
        self.frame_end = 250
        
    def create_whiteboard(self, width=10, height=8):
        """Create whiteboard plane"""
        bpy.ops.mesh.primitive_plane_add(size=1)
        board = bpy.context.active_object
        board.scale = (width/2, height/2, 1)
        board.name = "Whiteboard"
        
        # Material
        mat = bpy.data.materials.new(name="WhiteboardMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)
        board.data.materials.append(mat)
        
        return board
    
    def draw_circle(self, center, radius, color=(0.1, 0.1, 0.1, 1.0)):
        """Draw a circle"""
        vertices = []
        edges = []
        
        for i in range(32):
            angle = (i / 32) * 2 * 3.14159
            x = center.x + radius * __import__('math').cos(angle)
            y = center.y + radius * __import__('math').sin(angle)
            z = center.z + 0.01
            vertices.append((x, y, z))
            
            if i < 31:
                edges.append((i, i + 1))
            else:
                edges.append((i, 0))
        
        mesh = bpy.data.meshes.new("Circle")
        mesh.from_pydata(vertices, edges, [])
        
        obj = bpy.data.objects.new("Circle", mesh)
        bpy.context.collection.objects.link(obj)
        
        return obj
    
    def draw_line(self, start, end, color=(0, 0, 0, 1)):
        """Draw a line"""
        mesh = bpy.data.meshes.new("Line")
        mesh.from_pydata([start, end], [(0, 1)], [])
        
        obj = bpy.data.objects.new("Line", mesh)
        bpy.context.collection.objects.link(obj)
        
        return obj
    
    def animate_draw(self, obj, start_frame, end_frame):
        """Animate object appearing"""
        obj.scale = (0, 0, 1)
        obj.keyframe_insert(data_path="scale", frame=start_frame)
        
        obj.scale = (1, 1, 1)
        obj.keyframe_insert(data_path="scale", frame=end_frame)
    
    def render_animation(self, output_path="/tmp/animation.mp4"):
        """Set up rendering"""
        scene = bpy.context.scene
        scene.frame_start = self.frame_start
        scene.frame_end = self.frame_end
        scene.render.fps = 24
        scene.render.filepath = output_path
        scene.render.engine = 'EEVEE'

def main():
    """Main function"""
    animator = WhiteboardAnimator()
    
    # Create whiteboard
    board = animator.create_whiteboard(width=16, height=9)
    
    # Draw elements
    circle = animator.draw_circle(Vector((0, 0, 0)), radius=1.5)
    animator.animate_draw(circle, 1, 50)
    
    line = animator.draw_line(Vector((-2, 2, 0)), Vector((2, -2, 0)))
    animator.animate_draw(line, 60, 100)
    
    print("Whiteboard animation setup complete")

if __name__ == '__main__':
    main()
