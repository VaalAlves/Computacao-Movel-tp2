
class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.preferences = {
            "theme": "light"  # Default theme is light
        }
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.preferences["theme"]
        self.preferences["theme"] = "dark" if current_theme == "light" else "light"
        return self.preferences["theme"]
    
    def get_theme(self):
        """Get the current theme preference"""
        return self.preferences["theme"]
