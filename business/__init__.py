class DEAL:
    STATUS_CHOICES = [
        ("created", "Created"),
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled")
    ]
    TYPE_CHOICES = [
        ("cash", "Cash"),
        ("trade", "Trade")
    ]
class AD:
    SIZES = [
        ("quarter", "Quarter Page"),
        ("half", "Half Page"),
        ("full", "Full Page"),
        ("two", "Two Page Spread")
    ]
    PLACEMENTS = [
        ("inside_front", "Inside Front Cover"),
        ("opposite_inside_front", "Opposite Inside Front Cover"),
        ("inside_back", "Inside Back Cover"),
        ("opposite_inside_back", "Opposite Inside Back Cover"),
        ("back", "Back Cover"),
        ("two_page_centerfold", "Two Page Centerfold Spread")
    ]



