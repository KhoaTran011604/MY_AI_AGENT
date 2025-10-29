"""
Seed sample products to MongoDB
Run this to populate product database with sample e-commerce data
"""

from product_chatbot import ProductChatbot


def seed_sample_products():
    """Add sample products to database"""

    print("\n" + "="*60)
    print("SEEDING SAMPLE PRODUCTS")
    print("="*60 + "\n")

    try:
        print("Initializing chatbot...")
        bot = ProductChatbot()

        # Sample products - Vietnamese e-commerce
        sample_products = [
            # LAPTOPS
            {
                "name": "Laptop Dell XPS 13 9320",
                "description": "Laptop cao cấp Dell XPS 13 với thiết kế siêu mỏng nhẹ, màn hình InfinityEdge 13.4 inch, hiệu năng mạnh mẽ với Intel Core i7 thế hệ 12, RAM 16GB và SSD 512GB. Phù hợp cho doanh nhân và người làm việc di động.",
                "category": "Laptop",
                "brand": "Dell",
                "price": 32990000,
                "currency": "VND",
                "stock": 25,
                "specifications": {
                    "CPU": "Intel Core i7-1250U",
                    "RAM": "16GB LPDDR5",
                    "Storage": "512GB SSD",
                    "Display": "13.4 inch FHD+ (1920x1200)",
                    "Graphics": "Intel Iris Xe",
                    "Weight": "1.27 kg"
                },
                "images": ["dell-xps13-1.jpg", "dell-xps13-2.jpg"],
                "rating": 4.7,
                "tags": ["ultrabook", "business", "premium", "portable"]
            },
            {
                "name": "Laptop ASUS ROG Strix G15",
                "description": "Laptop gaming ASUS ROG Strix G15 với AMD Ryzen 9, RTX 4060, màn hình 15.6 inch 165Hz, hệ thống tản nhiệt ROG Intelligent Cooling. Mang lại trải nghiệm chơi game mượt mà và đồ họa ấn tượng.",
                "category": "Laptop",
                "brand": "ASUS",
                "price": 35990000,
                "currency": "VND",
                "stock": 15,
                "specifications": {
                    "CPU": "AMD Ryzen 9 7945HX",
                    "RAM": "32GB DDR5",
                    "Storage": "1TB SSD",
                    "Display": "15.6 inch FHD (1920x1080) 165Hz",
                    "Graphics": "NVIDIA RTX 4060 8GB",
                    "Weight": "2.5 kg"
                },
                "images": ["asus-rog-g15-1.jpg"],
                "rating": 4.8,
                "tags": ["gaming", "high-performance", "rgb"]
            },
            {
                "name": "MacBook Air M2 2023",
                "description": "MacBook Air với chip M2 mới nhất, thiết kế mỏng nhẹ, màn hình Liquid Retina 13.6 inch, thời lượng pin lên đến 18 giờ. Lý tưởng cho sinh viên, văn phòng và người sáng tạo nội dung.",
                "category": "Laptop",
                "brand": "Apple",
                "price": 28990000,
                "currency": "VND",
                "stock": 40,
                "specifications": {
                    "CPU": "Apple M2 8-core",
                    "RAM": "8GB Unified Memory",
                    "Storage": "256GB SSD",
                    "Display": "13.6 inch Liquid Retina (2560x1664)",
                    "Graphics": "Apple M2 10-core GPU",
                    "Weight": "1.24 kg"
                },
                "images": ["macbook-air-m2-1.jpg", "macbook-air-m2-2.jpg"],
                "rating": 4.9,
                "tags": ["apple", "lightweight", "long-battery", "creator"]
            },
            {
                "name": "Laptop HP Pavilion 15",
                "description": "Laptop HP Pavilion 15 với thiết kế thanh lịch, hiệu năng ổn định cho học tập và làm việc văn phòng. Màn hình 15.6 inch FHD, Intel Core i5 thế hệ 12, giá cả phải chăng.",
                "category": "Laptop",
                "brand": "HP",
                "price": 15990000,
                "currency": "VND",
                "stock": 35,
                "specifications": {
                    "CPU": "Intel Core i5-1235U",
                    "RAM": "8GB DDR4",
                    "Storage": "512GB SSD",
                    "Display": "15.6 inch FHD (1920x1080)",
                    "Graphics": "Intel UHD Graphics",
                    "Weight": "1.75 kg"
                },
                "images": ["hp-pavilion-15-1.jpg"],
                "rating": 4.3,
                "tags": ["budget", "student", "office"]
            },

            # SMARTPHONES
            {
                "name": "iPhone 15 Pro Max",
                "description": "iPhone 15 Pro Max với chip A17 Pro, camera 48MP, màn hình Super Retina XDR 6.7 inch, khung titan cao cấp. Điện thoại flagship hàng đầu của Apple với hiệu năng vượt trội.",
                "category": "Điện thoại",
                "brand": "Apple",
                "price": 34990000,
                "currency": "VND",
                "stock": 50,
                "specifications": {
                    "Screen": "6.7 inch Super Retina XDR OLED",
                    "Chipset": "Apple A17 Pro",
                    "RAM": "8GB",
                    "Storage": "256GB",
                    "Camera": "48MP + 12MP + 12MP",
                    "Battery": "4422 mAh"
                },
                "images": ["iphone-15-pro-max-1.jpg", "iphone-15-pro-max-2.jpg"],
                "rating": 4.9,
                "tags": ["flagship", "premium", "ios", "5g"]
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "description": "Samsung Galaxy S24 Ultra với bút S Pen tích hợp, camera 200MP, màn hình Dynamic AMOLED 2X 6.8 inch, chip Snapdragon 8 Gen 3. Smartphone Android cao cấp nhất của Samsung.",
                "category": "Điện thoại",
                "brand": "Samsung",
                "price": 33990000,
                "currency": "VND",
                "stock": 45,
                "specifications": {
                    "Screen": "6.8 inch Dynamic AMOLED 2X",
                    "Chipset": "Snapdragon 8 Gen 3",
                    "RAM": "12GB",
                    "Storage": "256GB",
                    "Camera": "200MP + 50MP + 12MP + 10MP",
                    "Battery": "5000 mAh"
                },
                "images": ["samsung-s24-ultra-1.jpg"],
                "rating": 4.8,
                "tags": ["flagship", "android", "s-pen", "camera"]
            },
            {
                "name": "Xiaomi 14 Pro",
                "description": "Xiaomi 14 Pro với camera Leica, màn hình AMOLED 6.73 inch 120Hz, chip Snapdragon 8 Gen 3, sạc nhanh 120W. Điện thoại cao cấp với giá cạnh tranh.",
                "category": "Điện thoại",
                "brand": "Xiaomi",
                "price": 19990000,
                "currency": "VND",
                "stock": 60,
                "specifications": {
                    "Screen": "6.73 inch AMOLED 120Hz",
                    "Chipset": "Snapdragon 8 Gen 3",
                    "RAM": "12GB",
                    "Storage": "256GB",
                    "Camera": "50MP Leica + 50MP + 50MP",
                    "Battery": "4880 mAh"
                },
                "images": ["xiaomi-14-pro-1.jpg"],
                "rating": 4.6,
                "tags": ["mid-premium", "fast-charging", "leica-camera"]
            },
            {
                "name": "OPPO Reno11 5G",
                "description": "OPPO Reno11 5G với thiết kế mỏng nhẹ, camera 50MP, màn hình AMOLED 6.7 inch, chip Dimensity 8200. Điện thoại tầm trung với camera ấn tượng và thiết kế đẹp mắt.",
                "category": "Điện thoại",
                "brand": "OPPO",
                "price": 10990000,
                "currency": "VND",
                "stock": 80,
                "specifications": {
                    "Screen": "6.7 inch AMOLED",
                    "Chipset": "MediaTek Dimensity 8200",
                    "RAM": "8GB",
                    "Storage": "256GB",
                    "Camera": "50MP + 32MP + 8MP",
                    "Battery": "5000 mAh"
                },
                "images": ["oppo-reno11-1.jpg"],
                "rating": 4.4,
                "tags": ["mid-range", "camera", "design"]
            },

            # TABLETS
            {
                "name": "iPad Pro 12.9 inch M2",
                "description": "iPad Pro 12.9 inch với chip M2, màn hình Liquid Retina XDR, hỗ trợ Apple Pencil thế hệ 2. Máy tính bảng cao cấp cho công việc sáng tạo và giải trí.",
                "category": "Máy tính bảng",
                "brand": "Apple",
                "price": 31990000,
                "currency": "VND",
                "stock": 20,
                "specifications": {
                    "Screen": "12.9 inch Liquid Retina XDR",
                    "Chipset": "Apple M2",
                    "RAM": "8GB",
                    "Storage": "256GB",
                    "Camera": "12MP + 10MP",
                    "Battery": "10758 mAh"
                },
                "images": ["ipad-pro-12-1.jpg"],
                "rating": 4.8,
                "tags": ["premium", "creator", "apple-pencil"]
            },
            {
                "name": "Samsung Galaxy Tab S9",
                "description": "Samsung Galaxy Tab S9 với màn hình Dynamic AMOLED 2X 11 inch, chip Snapdragon 8 Gen 2, bút S Pen đi kèm. Máy tính bảng Android cao cấp cho công việc và giải trí.",
                "category": "Máy tính bảng",
                "brand": "Samsung",
                "price": 19990000,
                "currency": "VND",
                "stock": 30,
                "specifications": {
                    "Screen": "11 inch Dynamic AMOLED 2X 120Hz",
                    "Chipset": "Snapdragon 8 Gen 2",
                    "RAM": "8GB",
                    "Storage": "128GB",
                    "Camera": "13MP + 12MP",
                    "Battery": "8400 mAh"
                },
                "images": ["galaxy-tab-s9-1.jpg"],
                "rating": 4.6,
                "tags": ["android", "s-pen", "multimedia"]
            },

            # HEADPHONES
            {
                "name": "AirPods Pro Gen 2",
                "description": "AirPods Pro thế hệ 2 với chip H2, chống ồn chủ động nâng cao, âm thanh spatial audio, hộp sạc MagSafe. Tai nghe true wireless cao cấp của Apple.",
                "category": "Tai nghe",
                "brand": "Apple",
                "price": 6490000,
                "currency": "VND",
                "stock": 100,
                "specifications": {
                    "Type": "True Wireless",
                    "Chip": "Apple H2",
                    "ANC": "Active Noise Cancellation",
                    "Battery": "Up to 6 hours (with ANC)",
                    "Water Resistance": "IPX4"
                },
                "images": ["airpods-pro-2-1.jpg"],
                "rating": 4.7,
                "tags": ["wireless", "anc", "premium", "ios"]
            },
            {
                "name": "Sony WH-1000XM5",
                "description": "Sony WH-1000XM5 với chống ồn hàng đầu thế giới, âm thanh Hi-Res, pin 30 giờ, thiết kế thoải mái. Tai nghe over-ear cao cấp cho audiophile.",
                "category": "Tai nghe",
                "brand": "Sony",
                "price": 8990000,
                "currency": "VND",
                "stock": 40,
                "specifications": {
                    "Type": "Over-ear Wireless",
                    "ANC": "Industry-leading Noise Cancellation",
                    "Battery": "Up to 30 hours",
                    "Audio": "Hi-Res Audio, LDAC",
                    "Weight": "250g"
                },
                "images": ["sony-wh1000xm5-1.jpg"],
                "rating": 4.9,
                "tags": ["wireless", "anc", "audiophile", "premium"]
            },

            # SMARTWATCHES
            {
                "name": "Apple Watch Series 9",
                "description": "Apple Watch Series 9 với chip S9, màn hình Always-On Retina, tính năng sức khỏe toàn diện, GPS tích hợp. Đồng hồ thông minh tốt nhất cho người dùng iPhone.",
                "category": "Đồng hồ thông minh",
                "brand": "Apple",
                "price": 10990000,
                "currency": "VND",
                "stock": 55,
                "specifications": {
                    "Display": "Always-On Retina LTPO OLED",
                    "Size": "45mm",
                    "Chip": "Apple S9 SiP",
                    "Sensors": "Heart rate, ECG, Blood oxygen, Temperature",
                    "Battery": "Up to 18 hours",
                    "Water Resistance": "50m"
                },
                "images": ["apple-watch-s9-1.jpg"],
                "rating": 4.8,
                "tags": ["smartwatch", "fitness", "health", "ios"]
            },
            {
                "name": "Samsung Galaxy Watch 6",
                "description": "Samsung Galaxy Watch 6 với màn hình AMOLED 1.5 inch, cảm biến BioActive, pin 2 ngày, tương thích Android. Đồng hồ thông minh toàn diện cho người dùng Samsung.",
                "category": "Đồng hồ thông minh",
                "brand": "Samsung",
                "price": 6990000,
                "currency": "VND",
                "stock": 45,
                "specifications": {
                    "Display": "1.5 inch Super AMOLED",
                    "Size": "44mm",
                    "Chipset": "Exynos W930",
                    "Sensors": "Heart rate, ECG, Body composition",
                    "Battery": "Up to 40 hours",
                    "Water Resistance": "5ATM"
                },
                "images": ["galaxy-watch-6-1.jpg"],
                "rating": 4.5,
                "tags": ["smartwatch", "fitness", "android"]
            }
        ]

        # Add products to database
        print(f"Adding {len(sample_products)} products...\n")

        for i, product in enumerate(sample_products, 1):
            product_id = bot.add_product(
                name=product['name'],
                description=product['description'],
                category=product['category'],
                brand=product['brand'],
                price=product['price'],
                currency=product['currency'],
                stock=product['stock'],
                specifications=product['specifications'],
                images=product['images'],
                rating=product['rating'],
                tags=product['tags']
            )
            print(f"  [{i}/{len(sample_products)}] Added: {product['name']}")

        print("\n" + "="*60)
        print("SEEDING COMPLETED")
        print("="*60)

        # Show statistics
        stats = bot.get_statistics()
        print(f"\nProduct Database:")
        print(f"  Total Products: {stats['total_products']}")
        print(f"  In Stock: {stats['in_stock']}")
        print(f"  Categories: {', '.join(stats['categories'])}")
        print(f"  Brands: {', '.join(stats['brands'])}")
        print(f"  Price Range: {stats['price_range']['min']:,.0f} - {stats['price_range']['max']:,.0f} VND")

        print("\n✓ Sample products seeded successfully!")
        print("\nYou can now:")
        print("  1. Run: python product_chatbot.py (CLI chat)")
        print("  2. Run: python product_chatbot_api.py (API server)")
        print("\nTry asking:")
        print("  - 'Tìm laptop dưới 20 triệu'")
        print("  - 'So sánh iPhone 15 và Samsung S24'")
        print("  - 'Tai nghe chống ồn tốt nhất'")

        bot.close()

    except Exception as e:
        print(f"\n✗ Error seeding products: {e}")
        print("\nPlease check:")
        print("  1. MongoDB is running")
        print("  2. MONGODB_URI in .env is correct")
        print("  3. All dependencies are installed")


if __name__ == "__main__":
    seed_sample_products()
