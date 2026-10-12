import logging
from sqlalchemy.orm import Session
from backend.app.database import engine, Base, SessionLocal
from backend.app.models import Destination, TransportRoute, Hotel, Restaurant, Attraction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("tripwise.seed")

DEMO_LABEL = "Demo data — illustrative estimates, not verified listings or bookable prices."

def seed_database(db: Session = None):
    """
    Populates SQLite database with transparently labeled sample seed records
    for 5 Indian destinations with complete transport routes, hotels, restaurants, and sights.
    """
    owns_session = False
    if db is None:
        Base.metadata.create_all(bind=engine)
        db = SessionLocal()
        owns_session = True

    try:
        from backend.app.services.data_importer import import_all_datasets

        # Check if already seeded
        existing_dest = db.query(Destination).filter(Destination.name == "Rishikesh").first()
        if existing_dest:
            logger.info("Database already seeded with demo data. Checking extended destinations and data layer...")
            seed_extended_destinations(db)
            import_all_datasets(db)
            return

        logger.info("Seeding database with verified demo destinations and routes...")

        # -------------------------------------------------------------------------
        # 1. RISHIKESH (Uttarakhand) - Nature, Adventure, Spirituality, Local Food
        # -------------------------------------------------------------------------
        rishikesh = Destination(
            name="Rishikesh",
            state="Uttarakhand",
            region="North India",
            category="Nature;Spirituality;Adventure;Food",
            trip_types="Nature, Spiritual, Adventure, Food, Wellness",
            best_seasons="Autumn, Winter, Spring (Sep-Apr)",
            ideal_days=3,
            minimum_days=2,
            maximum_days=5,
            popularity_score=9.2,
            safety_rating=8.8,
            nearest_major_city="Dehradun",
            nearest_airport="Jolly Grant Airport, Dehradun (21 km)",
            nearest_railway="Yog Nagari Rishikesh Railway Station",
            latitude=30.0869,
            longitude=78.2676,
            description="Yoga capital of the world located on the banks of the sacred Ganges in the Himalayan foothills. Renowned for scenic riverbanks, pristine nature, Ayurvedic food, and river rafting.",
            suggested_itinerary_text="Day 1: Ganga Aarti at Triveni Ghat & Ram Jhula; Day 2: Neer Garh Waterfall, riverside cafe hopping & local food; Day 3: Beatles Ashram & scenic nature viewpoints.",
            source_dataset="sushanthnaidu24/indian-tourism-dataset",
            data_status="historical"
        )
        db.add(rishikesh)
        db.flush()

        # Routes to Rishikesh
        db.add_all([
            TransportRoute(
                origin_city="Delhi",
                destination_id=rishikesh.id,
                mode="Jan Shatabdi / Vande Bharat Express",
                duration_hours=4.5,
                amount_inr=1450,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Standard AC Chair Car round-trip train estimate from New Delhi to Haridwar/Rishikesh."
            ),
            TransportRoute(
                origin_city="Delhi",
                destination_id=rishikesh.id,
                mode="Deluxe AC Volvo Bus",
                duration_hours=5.5,
                amount_inr=1100,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Overnight Volvo intercity bus round-trip from ISBT Kashmiri Gate."
            ),
            TransportRoute(
                origin_city="Mumbai",
                destination_id=rishikesh.id,
                mode="Economy Flight + Dehradun Taxi",
                duration_hours=4.0,
                amount_inr=8500,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Illustrative off-peak flight via DED airport."
            )
        ])

        # Hotels in Rishikesh (clearly labeled sample entries)
        db.add_all([
            Hotel(
                destination_id=rishikesh.id,
                name="Ganga Nature Riverside Retreat [Sample Stay]",
                city="Rishikesh",
                stars="3-star equivalent",
                rating=4.4,
                amenities="River view, Free Wi-Fi, Mountain deck, Pure veg cafe",
                tier="Budget",
                amount_inr=1850,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            ),
            Hotel(
                destination_id=rishikesh.id,
                name="Tapovan Foothills Boutique Stay [Sample Stay]",
                city="Rishikesh",
                stars="3-star",
                rating=4.6,
                amenities="Yoga hall, Wi-Fi, Organic breakfast, AC",
                tier="Mid-range",
                amount_inr=2900,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        # Restaurants in Rishikesh
        db.add_all([
            Restaurant(
                destination_id=rishikesh.id,
                name="Chotiwala Heritage Restaurant [Sample Listing]",
                city="Rishikesh",
                cuisine="Garhwali & Traditional North Indian Thali",
                price_band="Budget",
                rating=4.3,
                location="Swarg Ashram, Ram Jhula",
                famous_dish="Garhwali Jhangora Kheer & Thali",
                amount_inr=220,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            ),
            Restaurant(
                destination_id=rishikesh.id,
                name="The Beatles Organic Cafe [Sample Listing]",
                city="Rishikesh",
                cuisine="Organic Mountain Cuisine & Smoothies",
                price_band="Mid",
                rating=4.5,
                location="Paidal Marg, Tapovan",
                famous_dish="Wood-fired sourdough & Himalayan Mint Tea",
                amount_inr=320,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        # Attractions in Rishikesh
        db.add_all([
            Attraction(
                destination_id=rishikesh.id,
                name="Neer Garh Waterfall & Nature Trail",
                category="Nature",
                opening_time="08:00 AM - 05:00 PM",
                est_duration_hours=2.5,
                recommended_time_of_day="Morning",
                area_cluster="Neer Forest Belt",
                description="Natural cascading mountain waterfall surrounded by lush canopy with refreshing rock pools.",
                amount_inr=50,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=rishikesh.id,
                name="Triveni Ghat Evening Maha Aarti",
                category="Spirituality",
                opening_time="05:30 PM - 07:30 PM",
                est_duration_hours=1.5,
                recommended_time_of_day="Evening",
                area_cluster="Ganga Riverfront",
                description="Mesmerizing lamps, Vedic chants, and floating earthen diyas along the sacred confluence.",
                amount_inr=0,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=rishikesh.id,
                name="The Beatles Ashram (Chaurasi Kutia)",
                category="Culture",
                opening_time="09:00 AM - 04:00 PM",
                est_duration_hours=2.0,
                recommended_time_of_day="Morning",
                area_cluster="Rajaji Tiger Reserve Zone",
                description="Historic meditation cave complex with vibrant graffiti murals where the Beatles wrote the White Album.",
                amount_inr=150,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=rishikesh.id,
                name="Ram Jhula & Laxman Jhula Suspension Bridges",
                category="Landmark",
                opening_time="Open 24 hours",
                est_duration_hours=1.5,
                recommended_time_of_day="Afternoon",
                area_cluster="Swarg Ashram Belt",
                description="Pedestrian iron suspension bridges offering panoramic vistas of the Ganges and Himalayan foothills.",
                amount_inr=0,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            )
        ])

        # -------------------------------------------------------------------------
        # 2. JAIPUR (Rajasthan) - Culture, Heritage, Food, Architecture
        # -------------------------------------------------------------------------
        jaipur = Destination(
            name="Jaipur",
            state="Rajasthan",
            region="North India",
            category="Culture;Heritage;Food;Architecture",
            trip_types="Cultural, Heritage, Food, Photography, Shopping",
            best_seasons="Winter (Oct-Mar)",
            ideal_days=3,
            minimum_days=2,
            maximum_days=4,
            popularity_score=9.5,
            safety_rating=8.6,
            nearest_major_city="Delhi (280 km)",
            nearest_airport="Jaipur International Airport",
            nearest_railway="Jaipur Junction",
            latitude=26.9124,
            longitude=75.7873,
            description="The Pink City of Rajasthan, famed for majestic hill forts, intricate royal palaces, and rich Rajasthani culinary heritage.",
            suggested_itinerary_text="Day 1: City Palace & Hawa Mahal; Day 2: Amber Fort & Jal Mahal; Day 3: Nahargarh Fort sunset & local bazaar food trail.",
            source_dataset="sushanthnaidu24/indian-tourism-dataset",
            data_status="historical"
        )
        db.add(jaipur)
        db.flush()

        db.add_all([
            TransportRoute(
                origin_city="Delhi",
                destination_id=jaipur.id,
                mode="Vande Bharat Express Train",
                duration_hours=3.5,
                amount_inr=1600,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Round-trip AC Chair Car ticket estimate Delhi to Jaipur Junction."
            ),
            TransportRoute(
                origin_city="Delhi",
                destination_id=jaipur.id,
                mode="Express Intercity Bus",
                duration_hours=5.0,
                amount_inr=950,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="RSRTC AC Volvo express service round-trip."
            ),
            TransportRoute(
                origin_city="Mumbai",
                destination_id=jaipur.id,
                mode="Superfast Train (AC 3-Tier)",
                duration_hours=16.0,
                amount_inr=2400,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Round trip overnight train from Mumbai Central."
            )
        ])

        db.add_all([
            Hotel(
                destination_id=jaipur.id,
                name="Haveli Heritage Inn [Sample Stay]",
                city="Jaipur",
                stars="3-star",
                rating=4.3,
                amenities="Courtyard garden, Free Wi-Fi, Rajasthani decor, AC",
                tier="Budget",
                amount_inr=1900,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            ),
            Hotel(
                destination_id=jaipur.id,
                name="Royal Rajputana Palace Hotel [Sample Stay]",
                city="Jaipur",
                stars="4-star",
                rating=4.6,
                amenities="Swimming pool, Rooftop restaurant, Spa, AC",
                tier="Mid-range",
                amount_inr=3600,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Restaurant(
                destination_id=jaipur.id,
                name="LMB - Laxmi Misthan Bhandar [Sample Listing]",
                city="Jaipur",
                cuisine="Authentic Rajasthani & Sweets",
                price_band="Budget",
                rating=4.4,
                location="Johari Bazaar, Old City",
                famous_dish="Dal Baati Churma & Ghewar",
                amount_inr=280,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            ),
            Restaurant(
                destination_id=jaipur.id,
                name="Rawat Misthan Heritage [Sample Listing]",
                city="Jaipur",
                cuisine="Street Food & Traditional Savouries",
                price_band="Budget",
                rating=4.5,
                location="Station Road, Sindhi Camp",
                famous_dish="Crispy Pyaaz Kachori & Mawa Kachori",
                amount_inr=160,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Attraction(
                destination_id=jaipur.id,
                name="Amber Fort & Palace",
                category="Heritage",
                opening_time="08:00 AM - 05:30 PM",
                est_duration_hours=3.0,
                recommended_time_of_day="Morning",
                area_cluster="Amer Hilltops",
                description="Grand 16th-century fortress overlooking Maota Lake, famous for Sheesh Mahal (Mirror Palace).",
                amount_inr=100,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=jaipur.id,
                name="Hawa Mahal (Palace of Winds)",
                category="Heritage",
                opening_time="09:00 AM - 05:00 PM",
                est_duration_hours=1.5,
                recommended_time_of_day="Morning",
                area_cluster="Old Walled City",
                description="Iconic five-story pink sandstone honeycomb facade with 953 jharokhas.",
                amount_inr=50,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=jaipur.id,
                name="Nahargarh Fort Sunset Viewpoint",
                category="Nature & Views",
                opening_time="10:00 AM - 06:30 PM",
                est_duration_hours=2.0,
                recommended_time_of_day="Evening",
                area_cluster="Aravalli Ridge",
                description="Panoramic views over the entire Pink City skyline from the Aravalli hills at sunset.",
                amount_inr=50,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            )
        ])

        # -------------------------------------------------------------------------
        # 3. AGRA (Uttar Pradesh) - Heritage, History, Food
        # -------------------------------------------------------------------------
        agra = Destination(
            name="Agra",
            state="Uttar Pradesh",
            region="North India",
            category="Heritage;Culture;Food",
            trip_types="Heritage, Cultural, Food, Photography",
            best_seasons="Winter (Oct-Mar)",
            ideal_days=2,
            minimum_days=1,
            maximum_days=3,
            popularity_score=9.6,
            safety_rating=8.2,
            nearest_major_city="Delhi (210 km)",
            nearest_airport="Agra Airport (Kheria)",
            nearest_railway="Agra Cantt",
            latitude=27.1767,
            longitude=78.0081,
            description="Home to the immortal Taj Mahal, UNESCO World Heritage Mughal forts, and legendary Mughlai and Petha sweet traditions.",
            suggested_itinerary_text="Day 1: Sunrise at Taj Mahal & Agra Fort; Day 2: Mehtab Bagh & Fatehpur Sikri excursion.",
            source_dataset="sushanthnaidu24/indian-tourism-dataset",
            data_status="historical"
        )
        db.add(agra)
        db.flush()

        db.add_all([
            TransportRoute(
                origin_city="Delhi",
                destination_id=agra.id,
                mode="Gatimaan Express Train",
                duration_hours=1.7,
                amount_inr=1500,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="High-speed executive chair car round trip from Hazrat Nizamuddin to Agra Cantt."
            ),
            TransportRoute(
                origin_city="Delhi",
                destination_id=agra.id,
                mode="Yamuna Expressway Deluxe Bus",
                duration_hours=3.5,
                amount_inr=800,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Direct express coach via Yamuna Expressway."
            )
        ])

        db.add_all([
            Hotel(
                destination_id=agra.id,
                name="Taj View Garden Guesthouse [Sample Stay]",
                city="Agra",
                stars="3-star",
                rating=4.2,
                amenities="Rooftop Taj view, Free Wi-Fi, Garden cafe, AC",
                tier="Budget",
                amount_inr=1650,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Restaurant(
                destination_id=agra.id,
                name="Panchi Petha & Mughlai Kitchen [Sample Listing]",
                city="Agra",
                cuisine="Mughlai & Authentic Agra Petha",
                price_band="Budget",
                rating=4.3,
                location="Taj Ganj, Agra",
                famous_dish="Bedmi Puri, Mughlai Paneer & Kesar Petha",
                amount_inr=200,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Attraction(
                destination_id=agra.id,
                name="Taj Mahal Monument",
                category="Heritage",
                opening_time="Sunrise to Sunset (Closed Fridays)",
                est_duration_hours=3.0,
                recommended_time_of_day="Morning",
                area_cluster="Taj Precinct",
                description="Peerless white marble mausoleum built by Emperor Shah Jahan on the banks of River Yamuna.",
                amount_inr=50, # Indian domestic ticket estimate
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=agra.id,
                name="Agra Fort (Red Fort)",
                category="Heritage",
                opening_time="06:00 AM - 06:00 PM",
                est_duration_hours=2.0,
                recommended_time_of_day="Afternoon",
                area_cluster="Yamuna Riverside",
                description="Walled imperial Mughal city in red sandstone containing Diwan-i-Khas and Jahangiri Mahal.",
                amount_inr=50,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            )
        ])

        # -------------------------------------------------------------------------
        # 4. GOA - Beach, Nature, Seafood, Nightlife
        # -------------------------------------------------------------------------
        goa = Destination(
            name="Goa",
            state="Goa",
            region="West India",
            category="Beach;Nature;Food;Nightlife",
            trip_types="Beach, Nature, Food, Nightlife, Culture",
            best_seasons="Winter, Post-Monsoon (Nov-Feb)",
            ideal_days=4,
            minimum_days=3,
            maximum_days=7,
            popularity_score=9.7,
            safety_rating=8.9,
            nearest_major_city="Mumbai (580 km)",
            nearest_airport="Dabolim / Manohar International Airport",
            nearest_railway="Madgaon / Thivim",
            latitude=15.2993,
            longitude=74.1240,
            description="Sun-kissed Arabian Sea coastline renowned for golden beaches, Portuguese architecture, coastal curries, and tropical greenery.",
            suggested_itinerary_text="Day 1: North Goa beaches (Anjuna, Vagator) & Chapora Fort; Day 2: Old Goa churches & Panjim Latin Quarter; Day 3: South Goa serene beaches (Palolem, Agonda); Day 4: Spice plantation & leisure.",
            source_dataset="sushanthnaidu24/indian-tourism-dataset",
            data_status="historical"
        )
        db.add(goa)
        db.flush()

        db.add_all([
            TransportRoute(
                origin_city="Mumbai",
                destination_id=goa.id,
                mode="Vande Bharat Express Train",
                duration_hours=7.5,
                amount_inr=2200,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Direct scenic Konkan Railway AC express round trip from CSMT to Madgaon."
            ),
            TransportRoute(
                origin_city="Bangalore",
                destination_id=goa.id,
                mode="Overnight AC Sleeper Bus",
                duration_hours=11.0,
                amount_inr=1800,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Comfortable overnight sleeper coach from Majestic."
            ),
            TransportRoute(
                origin_city="Delhi",
                destination_id=goa.id,
                mode="Economy Flight Round-Trip",
                duration_hours=2.5,
                amount_inr=7500,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Advance booking flight round-trip DEL to GOI."
            )
        ])

        db.add_all([
            Hotel(
                destination_id=goa.id,
                name="Calangute Coast Villa [Sample Stay]",
                city="Goa",
                stars="3-star",
                rating=4.2,
                amenities="Pool, Free Wi-Fi, Walk to beach, AC",
                tier="Budget",
                amount_inr=2100,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            ),
            Hotel(
                destination_id=goa.id,
                name="Palolem Palm Haven [Sample Stay]",
                city="Goa",
                stars="3-star",
                rating=4.5,
                amenities="Cottage style, Sea breeze, Free Wi-Fi",
                tier="Budget",
                amount_inr=2400,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Restaurant(
                destination_id=goa.id,
                name="Fisherman's Wharf & Shack [Sample Listing]",
                city="Goa",
                cuisine="Goan Coastal Seafood & Thali",
                price_band="Mid",
                rating=4.5,
                location="Sal Riverfront, South Goa",
                famous_dish="Goan Fish Curry Rice & Prawn Balchao",
                amount_inr=350,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Attraction(
                destination_id=goa.id,
                name="Fort Aguada & Coastal Lighthouse",
                category="Heritage & Sea Views",
                opening_time="09:00 AM - 06:00 PM",
                est_duration_hours=2.0,
                recommended_time_of_day="Morning",
                area_cluster="Sinquerim Coast",
                description="17th-century Portuguese fort standing on Sinquerim Beach overlooking the Arabian Sea.",
                amount_inr=50,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=goa.id,
                name="Old Goa Basilica of Bom Jesus",
                category="Heritage",
                opening_time="09:00 AM - 06:30 PM",
                est_duration_hours=1.5,
                recommended_time_of_day="Afternoon",
                area_cluster="Velha Goa",
                description="UNESCO World Heritage church containing the mortal remains of St. Francis Xavier.",
                amount_inr=0,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            )
        ])

        # -------------------------------------------------------------------------
        # 5. COORG / KOCHI (South India) - Nature, Plantations, Local Cuisine
        # -------------------------------------------------------------------------
        kochi = Destination(
            name="Kochi",
            state="Kerala",
            region="South India",
            category="Nature;Culture;Food;Heritage",
            trip_types="Nature, Culture, Food, Coastal, Heritage",
            best_seasons="Winter (Oct-Feb)",
            ideal_days=3,
            minimum_days=2,
            maximum_days=4,
            popularity_score=9.3,
            safety_rating=9.1,
            nearest_major_city="Bengaluru (550 km)",
            nearest_airport="Cochin International Airport (COK)",
            nearest_railway="Ernakulam Junction",
            latitude=9.9312,
            longitude=76.2673,
            description="The Queen of the Arabian Sea, blending historic Fort Kochi colonial streets, Chinese fishing nets, Kathakali dance, and Malabar coastal cuisine.",
            suggested_itinerary_text="Day 1: Fort Kochi walking tour, Chinese nets & St. Francis Church; Day 2: Mattancherry Palace & Jew Town spice bazaar; Day 3: Backwater canal cruise & Kathakali show.",
            source_dataset="sushanthnaidu24/indian-tourism-dataset",
            data_status="historical"
        )
        db.add(kochi)
        db.flush()

        db.add_all([
            TransportRoute(
                origin_city="Bangalore",
                destination_id=kochi.id,
                mode="KSRTC Airavat AC Bus",
                duration_hours=9.5,
                amount_inr=1900,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Round-trip overnight multi-axle Volvo from Bangalore to Ernakulam."
            ),
            TransportRoute(
                origin_city="Chennai",
                destination_id=kochi.id,
                mode="Superfast Express Train",
                duration_hours=11.0,
                amount_inr=1400,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="AC 3-Tier round-trip train from Chennai Central to Ernakulam."
            ),
            TransportRoute(
                origin_city="Delhi",
                destination_id=kochi.id,
                mode="Economy Flight Round-Trip",
                duration_hours=3.2,
                amount_inr=9200,
                price_unit="per_person_round_trip",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                notes="Round trip flight DEL to COK."
            )
        ])

        db.add_all([
            Hotel(
                destination_id=kochi.id,
                name="Fort Heritage Homestay [Sample Stay]",
                city="Kochi",
                stars="3-star",
                rating=4.5,
                amenities="Colonial architecture, Wi-Fi, Breakfast, AC",
                tier="Budget",
                amount_inr=1800,
                price_unit="per_room_per_night",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Restaurant(
                destination_id=kochi.id,
                name="Malabar Coastal Kitchen [Sample Listing]",
                city="Kochi",
                cuisine="Kerala Seafood & Appam Stew",
                price_band="Budget",
                rating=4.6,
                location="Fort Kochi, Princess Street",
                famous_dish="Karimeen Pollichathu & Appam with Stew",
                amount_inr=260,
                price_unit="per_person_per_meal",
                price_checked_on=None,
                source_url=None,
                data_status="demo",
                is_sample_entry=True
            )
        ])

        db.add_all([
            Attraction(
                destination_id=kochi.id,
                name="Fort Kochi Chinese Fishing Nets & Promenade",
                category="Heritage & Culture",
                opening_time="Open all day",
                est_duration_hours=2.0,
                recommended_time_of_day="Morning",
                area_cluster="Fort Kochi Waterfront",
                description="Cantilevered maritime fishing structures introduced by traders in the 14th century.",
                amount_inr=0,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            ),
            Attraction(
                destination_id=kochi.id,
                name="Mattancherry Palace (Dutch Palace)",
                category="Heritage",
                opening_time="10:00 AM - 05:00 PM (Closed Fridays)",
                est_duration_hours=1.5,
                recommended_time_of_day="Afternoon",
                area_cluster="Mattancherry",
                description="Historic royal palace featuring ornate mythological murals and Kochi coronation portraits.",
                amount_inr=20,
                price_unit="per_person_entry",
                price_checked_on="2025",
                data_status="historical"
            )
        ])

        db.commit()
        seed_extended_destinations(db)
        from backend.app.services.data_importer import import_all_datasets
        import_all_datasets(db)

    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding database: {e}")
        raise e
    finally:
        if owns_session:
            db.close()


def seed_extended_destinations(db: Session):
    """
    Ensures rich transport routes, hotels, and restaurants are seeded for top Indian destinations
    (Manali, Shimla, Udaipur, Varanasi, Amritsar, Munnar, Ooty, Ladakh, Gokarna, Darjeeling)
    and additional routes from major cities (Delhi, Mumbai, Bangalore, Chennai, Kolkata, Ahmedabad, Chandigarh).
    """
    try:
        # Check if extended destinations are already present and have routes
        manali_dest = db.query(Destination).filter(Destination.name == "Manali").first()
        if manali_dest:
            manali_route = db.query(TransportRoute).filter(TransportRoute.destination_id == manali_dest.id).first()
            if manali_route:
                return

        logger.info("Ensuring extended destinations exist and seeding routes, hotels, and restaurants...")

        # 0. Ensure Destination records exist (important for in-memory test databases or clean DBs)
        extended_dest_defs = [
            Destination(
                name="Manali",
                state="Himachal Pradesh",
                region="North India",
                category="Mountains;Snow;Adventure;Nature",
                trip_types="Honeymoon, Adventure, Nature, Mountain",
                best_seasons="All Season (Snow in Winter, pleasant in Summer)",
                ideal_days=4,
                minimum_days=3,
                maximum_days=6,
                popularity_score=9.3,
                safety_rating=8.9,
                nearest_major_city="Chandigarh",
                nearest_airport="Bhuntar Airport, Kullu (50 km)",
                nearest_railway="Chandigarh Railway Station (310 km)",
                description="High-altitude Himalayan resort town known for snow-capped peaks, Solang Valley adventure sports, and scenic pine forests.",
                suggested_itinerary_text="Day 1: Old Manali & Hadimba Temple; Day 2: Solang Valley & Atal Tunnel; Day 3: Vashisht hot springs & river cafe; Day 4: Naggar Castle.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Shimla",
                state="Himachal Pradesh",
                region="North India",
                category="Mountains;Colonial Heritage;Nature",
                trip_types="Heritage, Mountain, Family, Leisure",
                best_seasons="All Season (Snow in Winter, pleasant in Summer)",
                ideal_days=3,
                minimum_days=2,
                maximum_days=5,
                popularity_score=9.1,
                safety_rating=9.0,
                nearest_major_city="Chandigarh",
                nearest_airport="Jubarhati Airport, Shimla (22 km)",
                nearest_railway="Kalka Railway Station (90 km)",
                description="Queen of Hills, featuring colonial architecture, pedestrian-only Mall Road, Ridge viewpoints, and cedar pine forests.",
                suggested_itinerary_text="Day 1: Mall Road & The Ridge; Day 2: Jakhoo Temple & Kufri nature walk; Day 3: Viceregal Lodge & Tara Devi.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Udaipur",
                state="Rajasthan",
                region="West India",
                category="Heritage;Palaces;Lakes;Romantic",
                trip_types="Heritage, Romantic, Culture, Food",
                best_seasons="Autumn, Winter (Oct-Mar)",
                ideal_days=3,
                minimum_days=2,
                maximum_days=5,
                popularity_score=9.4,
                safety_rating=9.1,
                nearest_major_city="Ahmedabad",
                nearest_airport="Maharana Pratap Airport, Udaipur (22 km)",
                nearest_railway="Udaipur City Railway Station",
                description="The City of Lakes, celebrated for marble palaces, Lake Pichola boat cruises, and Mewari architectural grandeur.",
                suggested_itinerary_text="Day 1: City Palace & Lake Pichola sunset boat cruise; Day 2: Jagdish Temple, Saheliyon-ki-Bari & Bagore Ki Haveli; Day 3: Sajjangarh Monsoon Palace.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Varanasi (Kashi)",
                state="Uttar Pradesh",
                region="North India",
                category="Spirituality;Heritage;Culture;Food",
                trip_types="Spiritual, Culture, Heritage, Photography",
                best_seasons="Autumn, Winter, Spring (Oct-Mar)",
                ideal_days=3,
                minimum_days=2,
                maximum_days=4,
                popularity_score=9.5,
                safety_rating=8.6,
                nearest_major_city="Prayagraj",
                nearest_airport="Lal Bahadur Shastri Airport, Varanasi (25 km)",
                nearest_railway="Varanasi Junction / Pt Deen Dayal Upadhyaya",
                description="One of the world's oldest living cities, sanctified by the holy Ganges River, evening Ganga Aarti, and labyrinthine heritage alleys.",
                suggested_itinerary_text="Day 1: Dashashwamedh Ghat Ganga Aarti & street food walk; Day 2: Sunrise boat ride, Kashi Vishwanath & Assi Ghat; Day 3: Sarnath Buddhist pilgrimage.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Amritsar",
                state="Punjab",
                region="North India",
                category="Heritage;Spirituality;Culinary;Culture",
                trip_types="Spiritual, Food, Heritage, Family",
                best_seasons="Autumn, Winter, Spring (Oct-Mar)",
                ideal_days=2,
                minimum_days=2,
                maximum_days=3,
                popularity_score=9.2,
                safety_rating=9.2,
                nearest_major_city="Jalandhar",
                nearest_airport="Sri Guru Ram Dass Jee International Airport, Amritsar",
                nearest_railway="Amritsar Junction",
                description="Spiritual and cultural hub of Sikhism, world-famous for the Golden Temple, community langar, Wagah Border parade, and rich Punjabi cuisine.",
                suggested_itinerary_text="Day 1: Golden Temple & Langar, Jallianwala Bagh, Amritsari kulcha feast; Day 2: Wagah Border flag ceremony & Gobindgarh Fort.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Munnar",
                state="Kerala",
                region="South India",
                category="Nature;Tea Plantations;Hills;Peace",
                trip_types="Nature, Romantic, Relaxed, Family",
                best_seasons="Sep-May",
                ideal_days=3,
                minimum_days=2,
                maximum_days=4,
                popularity_score=9.1,
                safety_rating=9.4,
                nearest_major_city="Kochi",
                nearest_airport="Cochin International Airport (110 km)",
                nearest_railway="Aluva / Ernakulam Railway Station (120 km)",
                description="Scenic Western Ghats hill station enveloped in rolling green tea plantations, misty mountain peaks, and cool climate.",
                suggested_itinerary_text="Day 1: Tea museum, Mattupetty Dam & Echo Point; Day 2: Eravikulam National Park (Nilgiri Tahr) & Top Station view; Day 3: Spice plantation walk.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Ooty (Udhagamandalam)",
                state="Tamil Nadu",
                region="South India",
                category="Nature;Hills;Colonial;Botanical",
                trip_types="Family, Honeymoon, Nature, Scenic",
                best_seasons="All Season (Oct-Jun)",
                ideal_days=3,
                minimum_days=2,
                maximum_days=4,
                popularity_score=9.0,
                safety_rating=9.2,
                nearest_major_city="Coimbatore",
                nearest_airport="Coimbatore International Airport (88 km)",
                nearest_railway="Mettupalayam (Nilgiri Mountain Toy Train)",
                description="Queen of Nilgiri hills, featuring the UNESCO Nilgiri Toy Train, botanical gardens, pine forests, and chocolate factories.",
                suggested_itinerary_text="Day 1: Botanical Gardens, Ooty Lake boating; Day 2: Nilgiri Mountain Toy Train ride & Doddabetta Peak; Day 3: Pykara Falls & tea factory tour.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Ladakh (Leh)",
                state="Ladakh",
                region="North India",
                category="Adventure;Mountains;Culture;Buddhism",
                trip_types="Adventure, Photography, Trekking, Spiritual",
                best_seasons="Summer (May-Sep)",
                ideal_days=5,
                minimum_days=4,
                maximum_days=8,
                popularity_score=9.6,
                safety_rating=9.1,
                nearest_major_city="Srinagar",
                nearest_airport="Kushok Bakula Rimpochee Airport, Leh",
                nearest_railway="Jammu Tawi (700 km)",
                description="Land of high mountain passes, crystal-blue alpine lakes, ancient Buddhist monasteries, and dramatic Himalayan landscapes.",
                suggested_itinerary_text="Day 1: Acclimatization & Leh market; Day 2: Thiksey & Hemis monasteries; Day 3: Khardung La & Nubra Valley; Day 4: Pangong Tso Lake.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Gokarna",
                state="Karnataka",
                region="South India",
                category="Beaches;Peace;Spirituality;Nature",
                trip_types="Beaches, Relaxed, Nature, Spiritual",
                best_seasons="Oct-Apr",
                ideal_days=3,
                minimum_days=2,
                maximum_days=5,
                popularity_score=8.9,
                safety_rating=9.0,
                nearest_major_city="Mangalore",
                nearest_airport="Goa Dabolim / Manohar Airport (140 km)",
                nearest_railway="Gokarna Road Railway Station",
                description="Tranquil coastal temple town with pristine cliffside beaches like Om Beach, Kudle Beach, and relaxed coastal cafes.",
                suggested_itinerary_text="Day 1: Mahabaleshwar Temple & Kudle Beach sunset; Day 2: Om Beach, Half Moon & Paradise Beach trek; Day 3: Mirjan Fort & beach cafe relaxation.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
            Destination(
                name="Darjeeling",
                state="West Bengal",
                region="East India",
                category="Mountains;Tea;Colonial Heritage;Scenic",
                trip_types="Honeymoon, Nature, Heritage, Family",
                best_seasons="Oct-May",
                ideal_days=3,
                minimum_days=2,
                maximum_days=5,
                popularity_score=9.1,
                safety_rating=9.1,
                nearest_major_city="Siliguri",
                nearest_airport="Bagdogra Airport (70 km)",
                nearest_railway="New Jalpaiguri Railway Station (NJP)",
                description="Himalayan hill station famed for panoramic views of Kangchenjunga, aromatic world-class Darjeeling tea gardens, and the Darjeeling Himalayan Toy Train.",
                suggested_itinerary_text="Day 1: Tiger Hill sunrise over Kangchenjunga & Batasia Loop; Day 2: Himalayan Mountaineering Institute, Padmaja Naidu Zoo & Mall Road; Day 3: Happy Valley Tea Estate tour.",
                source_dataset="sushanthnaidu24/indian-tourism-dataset",
                data_status="historical"
            ),
        ]

        existing_names = {d.name for d in db.query(Destination).all()}
        for ed in extended_dest_defs:
            if ed.name not in existing_names:
                db.add(ed)
        db.flush()

        # Mapping of destination names to ID
        dests = {d.name: d.id for d in db.query(Destination).all()}

        routes_to_add = []
        hotels_to_add = []
        restaurants_to_add = []

        # 1. Manali
        m_id = dests.get("Manali")
        if m_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=m_id, mode="Deluxe AC Volvo Overnight Bus", duration_hours=12.0, amount_inr=1800, price_unit="per_person_round_trip", data_status="demo", notes="Overnight Volvo from Majnu Ka Tila / Kashmiri Gate to Manali Private Bus Stand."),
                TransportRoute(origin_city="Delhi", destination_id=m_id, mode="Vande Bharat to Chandigarh + Mountain Cab", duration_hours=9.5, amount_inr=2600, price_unit="per_person_round_trip", data_status="demo", notes="Fast rail to Chandigarh followed by scenic Himalayan highway cab."),
                TransportRoute(origin_city="Mumbai", destination_id=m_id, mode="Connecting Flight to Bhuntar/Kullu + Cab", duration_hours=5.0, amount_inr=8500, price_unit="per_person_round_trip", data_status="demo", notes="Flight via Delhi to Bhuntar Airport followed by 45 min valley cab."),
                TransportRoute(origin_city="Chandigarh", destination_id=m_id, mode="Intercity AC Volvo Bus", duration_hours=7.5, amount_inr=1100, price_unit="per_person_round_trip", data_status="demo", notes="Direct AC coach from Sector 43 ISBT.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=m_id, name="Himalayan Pine & Riverside Retreat [Sample Stay]", city="Manali", stars="3-star", rating=4.5, amenities="Beas river view, Balcony, Heated rooms, Mountain cafe", tier="Budget", amount_inr=1950, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=m_id, name="Solang Snowcrest Alpine Resort [Sample Stay]", city="Manali", stars="4-star", rating=4.7, amenities="Valley view, Wooden cottages, Fireplace, Spa, Buffet breakfast", tier="Mid-range", amount_inr=3200, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=m_id, name="Old Manali River & Tree Cafe [Sample Listing]", city="Manali", cuisine="Mountain Cafe, Trout Fish & Wood-fired Pizza", price_band="Mid", rating=4.6, location="Old Manali Village", famous_dish="Grilled Himalayan Trout & Apple Crumble", amount_inr=280, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=m_id, name="Chopsticks Himalayan Kitchen [Sample Listing]", city="Manali", cuisine="Tibetan, Thukpa & North Indian Comfort Food", price_band="Budget", rating=4.4, location="The Mall, Manali", famous_dish="Steamed Momos & Gyathuk Noodle Soup", amount_inr=220, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 2. Shimla
        s_id = dests.get("Shimla")
        if s_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=s_id, mode="Kalka Shatabdi + Himalayan Toy Train", duration_hours=6.5, amount_inr=1650, price_unit="per_person_round_trip", data_status="demo", notes="Scenic UNESCO Heritage toy train connection from Kalka."),
                TransportRoute(origin_city="Delhi", destination_id=s_id, mode="Deluxe AC Volvo Intercity Bus", duration_hours=7.5, amount_inr=1200, price_unit="per_person_round_trip", data_status="demo", notes="Overnight luxury sleeper/semi-sleeper from Delhi ISBT."),
                TransportRoute(origin_city="Mumbai", destination_id=s_id, mode="Economy Flight to Chandigarh + Taxi", duration_hours=4.5, amount_inr=7800, price_unit="per_person_round_trip", data_status="demo", notes="Direct flight from Mumbai to Chandigarh with shared tourist taxi up to Shimla."),
                TransportRoute(origin_city="Chandigarh", destination_id=s_id, mode="Himalayan AC Coach", duration_hours=3.5, amount_inr=600, price_unit="per_person_round_trip", data_status="demo", notes="Short intercity mountain highway bus.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=s_id, name="Mall Road Ridge View Inn [Sample Stay]", city="Shimla", stars="3-star", rating=4.3, amenities="Mall Road access, Valley balcony, Wi-Fi, Heating", tier="Budget", amount_inr=1850, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=s_id, name="Colonial Heritage Forest Lodge [Sample Stay]", city="Shimla", stars="4-star", rating=4.6, amenities="Cedar forest surroundings, Victorian lounge, Fireplace", tier="Mid-range", amount_inr=2900, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=s_id, name="Wake & Bake Cafe The Ridge [Sample Listing]", city="Shimla", cuisine="Artisan Cafe, Crepes & French Press Coffee", price_band="Mid", rating=4.5, location="The Mall, The Ridge", famous_dish="Hummus Pita & Hand-rolled Cinnamon Rolls", amount_inr=250, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=s_id, name="Baljee's Traditional Kitchen [Sample Listing]", city="Shimla", cuisine="Traditional North Indian & Himachali Sweets", price_band="Budget", rating=4.3, location="Lower Mall Road", famous_dish="Gulab Jamun & Chana Bhatura", amount_inr=200, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 3. Udaipur
        u_id = dests.get("Udaipur")
        if u_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=u_id, mode="Chetak Express AC 3-Tier Train", duration_hours=11.5, amount_inr=1700, price_unit="per_person_round_trip", data_status="demo", notes="Overnight AC train from Delhi Sarai Rohilla to Udaipur City."),
                TransportRoute(origin_city="Delhi", destination_id=u_id, mode="Direct Economy Flight", duration_hours=1.5, amount_inr=4500, price_unit="per_person_round_trip", data_status="demo", notes="Direct 1 hr 20 min flight from DEL to UDR."),
                TransportRoute(origin_city="Mumbai", destination_id=u_id, mode="Superfast AC Express Train", duration_hours=13.0, amount_inr=2100, price_unit="per_person_round_trip", data_status="demo", notes="Direct train from Bandra Terminus to Udaipur."),
                TransportRoute(origin_city="Mumbai", destination_id=u_id, mode="Direct Economy Flight", duration_hours=1.5, amount_inr=4200, price_unit="per_person_round_trip", data_status="demo", notes="Quick round-trip flight BOM to UDR."),
                TransportRoute(origin_city="Ahmedabad", destination_id=u_id, mode="Deluxe AC Intercity Bus", duration_hours=5.0, amount_inr=850, price_unit="per_person_round_trip", data_status="demo", notes="Comfortable highway bus via NH48.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=u_id, name="Pichola Lakeview Heritage Haveli [Sample Stay]", city="Udaipur", stars="3-star", rating=4.4, amenities="Rooftop Lake Pichola view, Courtyard, Wi-Fi, Rajasthani decor", tier="Budget", amount_inr=2100, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=u_id, name="Fateh Sagar Royal Palace Resort [Sample Stay]", city="Udaipur", stars="4-star", rating=4.7, amenities="Swimming pool, Lake view, Cultural folk dance, Heritage suites", tier="Mid-range", amount_inr=3600, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=u_id, name="Ambrai Waterfront Restaurant [Sample Listing]", city="Udaipur", cuisine="Royal Mewari Cuisine & Candlelight Dining", price_band="Mid", rating=4.6, location="Amet Haveli, Lake Pichola", famous_dish="Mewari Laal Maas & Gatte Ki Sabzi", amount_inr=350, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=u_id, name="Millets of Mewar Organic Eatery [Sample Listing]", city="Udaipur", cuisine="Healthy Traditional Rajasthani & Gluten-Free Thalis", price_band="Budget", rating=4.5, location="Hanuman Ghat", famous_dish="Bajra Khichdi & Ker Sangri", amount_inr=240, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 4. Varanasi (Kashi)
        v_id = dests.get("Varanasi (Kashi)")
        if v_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=v_id, mode="Vande Bharat Express", duration_hours=8.0, amount_inr=1750, price_unit="per_person_round_trip", data_status="demo", notes="High-speed flagship day train from New Delhi to Varanasi Junction."),
                TransportRoute(origin_city="Delhi", destination_id=v_id, mode="Shiv Ganga Express AC Train", duration_hours=11.5, amount_inr=1200, price_unit="per_person_round_trip", data_status="demo", notes="Overnight premier train connecting New Delhi and Varanasi."),
                TransportRoute(origin_city="Mumbai", destination_id=v_id, mode="Mahanagari Superfast Express", duration_hours=24.0, amount_inr=2400, price_unit="per_person_round_trip", data_status="demo", notes="Long-distance AC 3-Tier train from CSMT."),
                TransportRoute(origin_city="Kolkata", destination_id=v_id, mode="Poorva Express AC Train", duration_hours=9.5, amount_inr=1400, price_unit="per_person_round_trip", data_status="demo", notes="Superfast train from Howrah to Varanasi.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=v_id, name="Ghat View Heritage Kothi [Sample Stay]", city="Varanasi", stars="3-star", rating=4.4, amenities="Rooftop Ganges Aarti view, Classical morning music, Pure veg dining", tier="Budget", amount_inr=1650, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=v_id, name="Kashi Darshan Riverside Stay [Sample Stay]", city="Varanasi", stars="4-star", rating=4.6, amenities="Private boat pickup, AC suites, Spiritual library, Free Wi-Fi", tier="Mid-range", amount_inr=2700, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=v_id, name="Kashi Chaat Bhandar [Sample Listing]", city="Varanasi", cuisine="Famous Banarasi Street Delicacies & Chaat", price_band="Budget", rating=4.7, location="Godowlia Chowk", famous_dish="Tamatar Chaat & Palak Patta Chaat", amount_inr=160, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=v_id, name="Dolphin Rooftop Ganga Restaurant [Sample Listing]", city="Varanasi", cuisine="Panoramic Riverview North & South Indian Dining", price_band="Mid", rating=4.4, location="Man Mandir Ghat", famous_dish="Special Banarasi Thali & Malaiyo", amount_inr=240, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 5. Amritsar
        a_id = dests.get("Amritsar")
        if a_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=a_id, mode="Swarna Shatabdi Express", duration_hours=6.0, amount_inr=1400, price_unit="per_person_round_trip", data_status="demo", notes="Executive daytime express train to Amritsar Junction."),
                TransportRoute(origin_city="Delhi", destination_id=a_id, mode="Deluxe AC Volvo Overnight Bus", duration_hours=8.0, amount_inr=1100, price_unit="per_person_round_trip", data_status="demo", notes="Comfortable overnight sleeper from ISBT."),
                TransportRoute(origin_city="Mumbai", destination_id=a_id, mode="Golden Temple Superfast Train", duration_hours=26.0, amount_inr=2400, price_unit="per_person_round_trip", data_status="demo", notes="Daily train connection connecting Western India to Punjab.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=a_id, name="Golden Temple Heritage Inn [Sample Stay]", city="Amritsar", stars="3-star", rating=4.4, amenities="Walking distance to Golden Temple, 24-hr checkin, Wi-Fi", tier="Budget", amount_inr=1600, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=a_id, name="Amritsar Grand Heritage Hotel [Sample Stay]", city="Amritsar", stars="4-star", rating=4.6, amenities="Grand suites, Punjabi hospitality dining, Airport transfer", tier="Mid-range", amount_inr=2600, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=a_id, name="Kesar Da Dhaba [Sample Listing]", city="Amritsar", cuisine="Legendary Century-old Punjabi Vegetarian Dhaba", price_band="Budget", rating=4.6, location="Chowk Passian", famous_dish="Maa Ki Dal cooked for 12 hours & Laccha Paratha", amount_inr=200, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=a_id, name="Bhai Kulwant Singh Kulchian Wale [Sample Listing]", city="Amritsar", cuisine="Authentic Clay Tandoor Amritsari Kulcha", price_band="Budget", rating=4.5, location="Near Golden Temple", famous_dish="Crispy Aloo Pyaaz Kulcha with Chole & Lassi", amount_inr=140, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 6. Ladakh (Leh)
        l_id = dests.get("Ladakh (Leh)")
        if l_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Delhi", destination_id=l_id, mode="Direct Economy Flight Round-Trip", duration_hours=1.5, amount_inr=8500, price_unit="per_person_round_trip", data_status="demo", notes="Spectacular flight across Himalayan peaks into Leh Kushok Bakula Airport."),
                TransportRoute(origin_city="Mumbai", destination_id=l_id, mode="Connecting Economy Flight", duration_hours=4.5, amount_inr=11500, price_unit="per_person_round_trip", data_status="demo", notes="Fast morning flight via New Delhi to Leh.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=l_id, name="Stok View Eco Resort [Sample Stay]", city="Leh", stars="3-star", rating=4.5, amenities="Oxygen support, Traditional Ladakhi architecture, Solar heating", tier="Budget", amount_inr=2400, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=l_id, name="Grand Himalayan Dragon Hotel [Sample Stay]", city="Leh", stars="4-star", rating=4.8, amenities="Mountain panoramic deck, Central heating, Cultural shows", tier="Mid-range", amount_inr=3800, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=l_id, name="Tibetan Kitchen Leh [Sample Listing]", city="Leh", cuisine="Authentic Tibetan, Bhutanese & Ladakhi Dishes", price_band="Mid", rating=4.7, location="Fort Road, Leh", famous_dish="Steamed Mutton Momos, Thukpa & Butter Tea", amount_inr=250, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=l_id, name="Bon Appetit Mountain View [Sample Listing]", city="Leh", cuisine="Fusion Ladakhi & Wood-fired Pizzas", price_band="Mid", rating=4.6, location="Changspa Road", famous_dish="Buckwheat crepes & Apricot pie", amount_inr=350, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 7. Munnar
        mu_id = dests.get("Munnar")
        if mu_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Bangalore", destination_id=mu_id, mode="KSRTC AC Sleeper Bus", duration_hours=10.5, amount_inr=2100, price_unit="per_person_round_trip", data_status="demo", notes="Overnight AC sleeper bus via Coimbatore and Udumalpet."),
                TransportRoute(origin_city="Chennai", destination_id=mu_id, mode="Superfast Train to Aluva + Cab", duration_hours=11.0, amount_inr=2400, price_unit="per_person_round_trip", data_status="demo", notes="Express train followed by scenic mountain ghat drive."),
                TransportRoute(origin_city="Kochi", destination_id=mu_id, mode="AC Scenic Hill Bus / Cab", duration_hours=3.5, amount_inr=1100, price_unit="per_person_round_trip", data_status="demo", notes="Short 3.5 hr scenic drive past Cheeyappara Waterfalls."),
                TransportRoute(origin_city="Delhi", destination_id=mu_id, mode="Economy Flight to Kochi + Hill Cab", duration_hours=5.5, amount_inr=9200, price_unit="per_person_round_trip", data_status="demo", notes="Flight to COK followed by direct private mountain cab.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=mu_id, name="Tea Valley Mist Resort [Sample Stay]", city="Munnar", stars="3-star", rating=4.5, amenities="Tea estate views, Mist balcony, Campfire, Kerala cuisine", tier="Budget", amount_inr=1950, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=mu_id, name="Anamudi Hills Eco Lodge [Sample Stay]", city="Munnar", stars="4-star", rating=4.7, amenities="Valley infinity viewpoint, Cardamom trail walks, Spa", tier="Mid-range", amount_inr=3100, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=mu_id, name="Rapsy Restaurant Munnar [Sample Listing]", city="Munnar", cuisine="Famous Kerala Spiced Roast & Malabar Biryani", price_band="Budget", rating=4.4, location="Main Bazaar Munnar", famous_dish="Kerala Beef/Chicken Roast & Flaky Porotta", amount_inr=200, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=mu_id, name="Saravana Bhavan Tea Country [Sample Listing]", city="Munnar", cuisine="Pure Vegetarian Filter Coffee & Banana Leaf Meals", price_band="Budget", rating=4.3, location="Nullatanni", famous_dish="Ghee Roast Dosa & Kerala Sadhya", amount_inr=160, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 8. Ooty (Udhagamandalam)
        o_id = dests.get("Ooty (Udhagamandalam)")
        if o_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Bangalore", destination_id=o_id, mode="KSRTC Airavat AC Bus", duration_hours=7.5, amount_inr=1750, price_unit="per_person_round_trip", data_status="demo", notes="Comfortable day/night coach through Bandipur and Mudumalai forests."),
                TransportRoute(origin_city="Chennai", destination_id=o_id, mode="Nilgiri Express Train + Toy Train", duration_hours=10.0, amount_inr=1550, price_unit="per_person_round_trip", data_status="demo", notes="Heritage steam toy train up from Mettupalayam."),
                TransportRoute(origin_city="Kochi", destination_id=o_id, mode="Intercity AC Bus", duration_hours=6.5, amount_inr=1400, price_unit="per_person_round_trip", data_status="demo", notes="Scenic ride via Coimbatore & Nilgiri ghats.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=o_id, name="Nilgiri Pine Heritage Cottage [Sample Stay]", city="Ooty", stars="3-star", rating=4.4, amenities="Fireplace, Pine view, Lawn, English breakfast, Wi-Fi", tier="Budget", amount_inr=1850, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=o_id, name="Botanical View Highland Stay [Sample Stay]", city="Ooty", stars="4-star", rating=4.6, amenities="Private garden suites, Tea lounge, Golf course access", tier="Mid-range", amount_inr=2900, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=o_id, name="Earl's Secret Heritage Diner [Sample Listing]", city="Ooty", cuisine="Colonial Glasshouse Continental & Anglo-Indian", price_band="Mid", rating=4.6, location="Havelock Road", famous_dish="Shepherd's Pie & Chocolate Fudge", amount_inr=300, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=o_id, name="Nahar Sidewalk Cafe [Sample Listing]", city="Ooty", cuisine="Wood-fired Italian Pizzas & South Indian Thalis", price_band="Budget", rating=4.3, location="Commercial Road", famous_dish="Nilgiri Filter Coffee & Thin Crust Pizza", amount_inr=180, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # 9. Gokarna
        g_id = dests.get("Gokarna")
        if g_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Bangalore", destination_id=g_id, mode="Overnight AC Sleeper Bus", duration_hours=9.5, amount_inr=1800, price_unit="per_person_round_trip", data_status="demo", notes="Comfortable direct overnight private sleeper bus."),
                TransportRoute(origin_city="Mumbai", destination_id=g_id, mode="Matsyagandha Express Train", duration_hours=12.0, amount_inr=1950, price_unit="per_person_round_trip", data_status="demo", notes="Scenic Konkan Railway journey to Gokarna Road station."),
                TransportRoute(origin_city="Goa", destination_id=g_id, mode="Coastal Train / Tourist Cab", duration_hours=2.5, amount_inr=800, price_unit="per_person_round_trip", data_status="demo", notes="Short inter-state ride from South Goa.")
            ])
            hotels_to_add.extend([
                Hotel(destination_id=g_id, name="Kudle Beach Breeze Shack & Stay [Sample Stay]", city="Gokarna", stars="3-star", rating=4.4, amenities="Beachfront access, Sea view hammocks, Wi-Fi, Fresh cafe", tier="Budget", amount_inr=1700, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True),
                Hotel(destination_id=g_id, name="Om Beach Ocean Cliff Resort [Sample Stay]", city="Gokarna", stars="4-star", rating=4.7, amenities="Cliff infinity deck, Sunset lounge, Ayurveda spa", tier="Mid-range", amount_inr=2800, price_unit="per_room_per_night", data_status="demo", is_sample_entry=True)
            ])
            restaurants_to_add.extend([
                Restaurant(destination_id=g_id, name="Namaste Cafe Om Beach [Sample Listing]", city="Gokarna", cuisine="Coastal Seafood, Nutella Pancakes & Fresh Juices", price_band="Budget", rating=4.5, location="Om Beach Cliff", famous_dish="Kingfish Fry & Shakshuka", amount_inr=260, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True),
                Restaurant(destination_id=g_id, name="Chez Christophe French Bistro [Sample Listing]", city="Gokarna", cuisine="Fresh European Bakery & Seafood Salads", price_band="Mid", rating=4.5, location="Middle Beach", famous_dish="Handmade pasta & Fresh fruit tart", amount_inr=300, price_unit="per_person_per_meal", data_status="demo", is_sample_entry=True)
            ])

        # Additional connections for existing destinations
        j_id = dests.get("Jaipur")
        if j_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Bangalore", destination_id=j_id, mode="Direct Economy Flight", duration_hours=2.5, amount_inr=6800, price_unit="per_person_round_trip", data_status="demo", notes="Direct 2 hr 30 min flight BLR to JAI."),
                TransportRoute(origin_city="Kolkata", destination_id=j_id, mode="Pratham Swatantrata Superfast Train", duration_hours=22.0, amount_inr=2600, price_unit="per_person_round_trip", data_status="demo", notes="Direct AC train Howrah to Jaipur."),
                TransportRoute(origin_city="Ahmedabad", destination_id=j_id, mode="Ashram Superfast Express", duration_hours=9.0, amount_inr=1200, price_unit="per_person_round_trip", data_status="demo", notes="Overnight AC sleeper train.")
            ])

        goa_id = dests.get("Goa")
        if goa_id:
            routes_to_add.extend([
                TransportRoute(origin_city="Hyderabad", destination_id=goa_id, mode="Overnight AC Sleeper Bus", duration_hours=12.0, amount_inr=1900, price_unit="per_person_round_trip", data_status="demo", notes="Direct sleeper coach via Raichur."),
                TransportRoute(origin_city="Chennai", destination_id=goa_id, mode="Vasco Da Gama Superfast Express", duration_hours=18.0, amount_inr=2500, price_unit="per_person_round_trip", data_status="demo", notes="Overnight train to Madgaon."),
                TransportRoute(origin_city="Pune", destination_id=goa_id, mode="Deluxe AC Volvo Coach", duration_hours=9.5, amount_inr=1600, price_unit="per_person_round_trip", data_status="demo", notes="Overnight scenic highway ride via Kolhapur.")
            ])

        db.add_all(routes_to_add)
        db.add_all(hotels_to_add)
        db.add_all(restaurants_to_add)
        db.commit()
        logger.info(f"Successfully seeded extended destinations: {len(routes_to_add)} routes, {len(hotels_to_add)} hotels, {len(restaurants_to_add)} restaurants.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error seeding extended destinations: {e}")


if __name__ == "__main__":
    seed_database()

