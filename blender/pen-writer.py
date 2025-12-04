"""
Blender Pen Writer
Dynamic pen/writing engine for conceptual diagrams
Author: ŊOB Universe
"""

import bpy
import bmesh
from mathutils import Vector

class PenWriter:
    """Write text and create dynamic pen strokes"""
    
    def __init__(self):
        self.strokes = []
        self.text_objects = []
    
    def write_text(self, text, location, size=1.0, font_file=None):
        """Write text object in 3D space"""
        bpy.ops.object.text_add(location=location)
        text_obj = bpy.context.active_object
        text_obj.data.body = text
        text_obj.data.size = size
        text_obj.scale = (size, size, size)
        
        if font_file:
            text_obj.data.font = bpy.data.fonts.load(font_file)
        
        self.text_objects.append(text_obj)
        return text_obj
    
    def create_pen_stroke(self, points, thickness=0.1, color=(0, 0, 0, 1)):
        """Create a pen stroke from points"""
        curve = bpy.data.curves.new(name="PenStroke", type='CURVE')
        curve.dimensions = '3D'
        curve.resolution_u = 12
        
        polyline = curve.splines.new('POLY')
        polyline.points.add(len(points) - 1)
        
        for i, point in enumerate(points):
            polyline.points[i].co = (point.x, point.y, point.z, 1)
        
        curve_obj = bpy.data.objects.new("PenStroke", curve)
        bpy.context.collection.objects.link(curve_obj)
        
        # Bevel for thickness
        curve.bevel_depth = thickness / 2
        
        self.strokes.append(curve_obj)
        return curve_obj
    
    def draw_path(self, start, end, num_points=20):
        """Draw curved path between two points"""
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            # Quadratic interpolation for smooth curve
            point = start.lerp(end, t) + Vector((0, 0, 0.1 * __import__('math').sin(t * 3.14159)))
            points.append(point)
        
        return self.create_pen_stroke(points)
    
    def animate_write(self, text_obj, start_frame, end_frame):
        """Animate text being written"""
        text_obj.scale = (0.01, 0.01, 0.01)
        text_obj.keyframe_insert(data_path="scale", frame=start_frame)
        
        text_obj.scale = (1, 1, 1)
        text_obj.keyframe_insert(data_path="scale", frame=end_frame)
    
    def compose_diagram(self, title, elements):
        """Create a complete diagram with title and elements"""
        # Add title
        title_obj = self.write_text(title, Vector((0, 5, 0)), size=2.0)
        
        # Add elements
        for i, element in enumerate(elements):
            pos = Vector((i * 3 - 3, 0, 0))
            self.write_text(element, pos, size=1.0)
        
        print(f"Diagram '{title}' created with {len(elements)} elements")

def main():
    """Main function"""
    writer = PenWriter()
    
    # Write title
    title = writer.write_text("ŊOB Concepts", Vector((0, 5, 0)), size=2.0)
    
    # Draw paths
    writer.draw_path(Vector((-2, 0, 0)), Vector((2, 0, 0)))
    writer.draw_path(Vector((0, 2, 0)), Vector((0, -2, 0)))
    
    # Compose diagram
    concepts = ["Ripple", "Harmonic", "Emotion"]
    writer.compose_diagram("ŊOB Universe", concepts)
    
    print("Pen writer setup complete")

if __name__ == '__main__':
    main()
