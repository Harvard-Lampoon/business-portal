class CONTRACT:
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

    TYPE_CHOICES = [
        ("magazine", "Magazine"),
        ("newsletter", "Newsletter"),
        ("website", "Website"),
        ("flag", "Flag"),
        ("event", "Event"),
        ("popup", "Pop-Up"),
        ("other", "Other"),
    ]

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
    NEWSLETTER_SIZES = [
        ("box", "Box"),
        ("leaderboard", "Leaderboard")
    ]



