from ...Basics.Vectors import Vector2D
from ..component import Component

class Transform(Component):
    def __init__(self, name, position: Vector2D = Vector2D(0, 0), rotation: float = 0, scale: Vector2D = Vector2D(1, 1)):
        super().__init__(name)
        self.position = position  # Use Vector2D for position
        self.rotation = rotation  # Rotation in degrees
        self.scale = scale # Use Vector2D for scale

    def translate(self, dx, dy):
        """Move the transform by (dx, dy)."""
        self.position.x += dx
        self.position.y += dy

    def set_position(self, x, y):
        """Set the position to a new (x, y)."""
        self.position.x = x
        self.position.y = y

    def get_position(self):
        """Return the current position."""
        return (self.position.x, self.position.y)

    def rotate(self, angle):
        """Rotate the transform by a certain angle."""
        self.rotation += angle

    def set_rotation(self, angle):
        """Set the rotation to a new angle."""
        self.rotation = angle

    def get_rotation(self):
        """Return the current rotation."""
        return self.rotation

    def scale_by(self, sx, sy):
        """Scale the transform by (sx, sy)."""
        self.scale.x *= sx
        self.scale.y *= sy

    def set_scale(self, scale_x, scale_y):
        """Set the scale to a new value."""
        self.scale.x = scale_x
        self.scale.y = scale_y

    def get_scale(self):
        """Return the current scale."""
        return f"<[{self._id}] Transform: {self.name}, Position: {self.position}, Rotation: {self.rotation}, Scale: {self.scale}>"

    def __str__(self):
        return f"<[{self._id}] Transform: {self.name}, Position: {self.position}, Rotation: {self.rotation}, Scale: {self.scale}>"
