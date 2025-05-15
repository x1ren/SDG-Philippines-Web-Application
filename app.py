from flask import Flask, render_template, jsonify
import json
import requests
import os

app = Flask(__name__)


news_api = os.environ.get('NEWS_API_KEY')
print("NEWS_API_KEY:", news_api)  


sdg_titles = [
    "No Poverty", "Zero Hunger", "Good Health and Well-being", 
    "Quality Education", "Gender Equality", "Clean Water and Sanitation", 
    "Affordable and Clean Energy", "Decent Work and Economic Growth", 
    "Industry, Innovation, and Infrastructure", "Reduced Inequalities", 
    "Sustainable Cities and Communities", "Responsible Consumption and Production", 
    "Climate Action", "Life Below Water", "Life on Land", 
    "Peace, Justice, and Strong Institutions", "Partnerships for the Goals"
]

sdg_paragraphs = {
   
    "No Poverty": """
        In the Philippines, poverty remains a persistent issue affecting millions of families. According to the 
        Philippine Statistics Authority (PSA), around 18.1% of the population lived below the national poverty line 
        in 2021. The COVID-19 pandemic exacerbated economic vulnerabilities, particularly for daily wage earners 
        and rural communities. Despite government interventions like the Pantawid Pamilyang Pilipino Program (4Ps), 
        disparities in income, education, and access to services continue to hinder progress. Sustainable solutions 
        include strengthening social protection systems, improving access to livelihood programs, and empowering marginalized 
        communities through inclusive policies and grassroots development.
    """,
    "Zero Hunger": """
        Hunger and food insecurity remain critical problems in the Philippines, with millions of Filipinos lacking access 
        to nutritious food daily. The Global Hunger Index 2023 ranks the country in the “serious” category, reflecting 
        widespread undernutrition, especially among children. Malnutrition leads to stunting, wasting, and poor academic 
        performance, particularly in rural and conflict-affected areas. The government has responded with initiatives such 
        as the National Feeding Program and efforts to support local agriculture. However, addressing hunger sustainably 
        requires investment in resilient food systems, climate-adaptive farming, and reducing food waste at all levels of 
        the supply chain.
    """,
    "Good Health and Well-being": """
        The Philippine healthcare system has made strides in recent decades, yet it continues to face major challenges. 
        Access to quality healthcare is uneven, especially in geographically isolated and disadvantaged areas. Non-communicable 
        diseases, poor mental health services, and maternal mortality rates remain pressing concerns. The pandemic highlighted 
        both the resilience and fragility of the healthcare system. Universal Health Care (UHC) law, signed in 2019, aims 
        to provide equitable access to health services for all Filipinos. Achieving this goal requires increased health financing, 
        more healthcare workers, and improved infrastructure and education on preventive care.
    """,
    "Quality Education": """
        Education is a key driver for social mobility, yet many Filipino students face barriers such as inadequate facilities, 
        overcrowded classrooms, and a lack of resources. In rural areas, access to quality education is limited, with many children 
        dropping out due to financial constraints. The Department of Education (DepEd) has introduced reforms to improve education quality, 
        such as the K-12 program, which aims to provide a more comprehensive and globally competitive curriculum. However, 
        further investment in teacher training, school infrastructure, and digital literacy is essential to ensure inclusive and 
        equitable education for all.
    """,
    "Gender Equality": """
        Despite progress in gender rights, women in the Philippines still face significant challenges, including gender-based violence, 
        discrimination in the workplace, and limited political representation. The Philippines ranks 16th in the Global Gender Gap Report, 
        but challenges remain, particularly in rural and indigenous communities. Laws like the Magna Carta of Women and the Anti-Violence 
        Against Women and Children Act are steps forward, but enforcement remains inconsistent. Gender equality can be achieved by empowering 
        women and girls, ensuring equal opportunities in the workforce, and tackling cultural norms that perpetuate gender discrimination.
    """,
    "Clean Water and Sanitation": """
        Access to clean water and sanitation is crucial for public health, but millions of Filipinos still lack reliable access to safe drinking water. 
        Rural areas, especially in remote regions, face water supply issues that affect health and economic productivity. The government has launched programs 
        such as the National Water Supply and Sanitation Program, aiming to provide potable water to underserved areas. However, challenges like poor infrastructure, 
        contamination, and inadequate waste management require sustainable solutions. Investments in water resource management, community-based water systems, 
        and sanitation education are key to addressing these challenges.
    """,
    "Affordable and Clean Energy": """
        The Philippines faces an energy crisis due to increasing demand, inadequate infrastructure, and dependence on fossil fuels. 
        Renewable energy sources like solar and wind power have great potential, but their integration into the national grid remains 
        slow. The Energy Efficiency and Conservation Act and the Renewable Energy Act aim to increase the share of renewable energy in the energy mix. 
        However, challenges such as high energy costs, energy poverty, and limited access to off-grid solutions persist. Transitioning to clean, affordable energy 
        is essential for economic development, climate resilience, and achieving energy security.
    """,
    "Decent Work and Economic Growth": """
        The Philippine economy has grown steadily in recent years, but income inequality and underemployment continue to affect many Filipinos. 
        The informal sector remains a large part of the economy, with workers lacking job security, benefits, and fair wages. The government has prioritized 
        job creation through programs such as the “Build, Build, Build” infrastructure initiative. However, creating decent work requires a focus on labor rights, 
        improving education and skills training, and ensuring that growth is inclusive and benefits all sectors of society.
    """,
    "Industry, Innovation, and Infrastructure": """
        The Philippines’ infrastructure is underdeveloped compared to other Southeast Asian nations. The “Build, Build, Build” program aims to address infrastructure gaps, 
        but challenges such as urban congestion, inadequate transportation systems, and unreliable power grids remain. Innovation and digitalization also present opportunities for 
        growth in sectors such as manufacturing, agriculture, and technology. Investing in infrastructure development, fostering innovation, and increasing access to digital tools will 
        enable the Philippines to become more competitive on the global stage.
    """,
    "Reduced Inequalities": """
        Social inequality is a significant issue in the Philippines, where wealth and opportunity are concentrated in urban areas, leaving rural regions underdeveloped. 
        The government has introduced programs aimed at reducing inequality, such as the Conditional Cash Transfer (CCT) program, but disparities in income, 
        access to education, and healthcare remain. Addressing these inequalities requires policies focused on social inclusion, equal access to education and healthcare, 
        and greater opportunities for marginalized communities to participate in the economy and society.
    """,
    "Sustainable Cities and Communities": """
        Urbanization in the Philippines has led to overcrowded cities with inadequate infrastructure, poor air quality, and inadequate housing for many residents. 
        Metro Manila is one of the most densely populated cities in the world, and informal settlements continue to expand. Sustainable urban development requires 
        investments in public transportation, affordable housing, waste management, and green spaces. Creating resilient cities also involves addressing climate change impacts 
        and improving disaster preparedness.
    """,
    "Responsible Consumption and Production": """
        The Philippines faces significant challenges in managing waste, with millions of tons of garbage generated annually. Waste management systems are often inadequate, 
        and recycling rates are low. The government has introduced policies like the Ecological Solid Waste Management Act to encourage sustainable consumption and waste 
        reduction. However, there is still a need for greater consumer awareness, more efficient recycling systems, and industry-led innovations to reduce resource use 
        and minimize environmental harm.
    """,
    "Climate Action": """
        The Philippines is one of the most disaster-prone countries in the world, facing frequent typhoons, flooding, and earthquakes. The effects of climate change—rising 
        temperatures, stronger storms, and sea-level rise—pose a significant threat to the country’s economy and citizens. The government has taken steps to address climate 
        change through the National Climate Change Action Plan (NCCAP), but progress is slow. Achieving climate resilience requires investments in renewable energy, 
        disaster preparedness, and community-based climate adaptation strategies.
    """,
    "Life Below Water": """
        The Philippines, with its vast marine resources, is home to some of the most biodiverse ecosystems in the world. However, overfishing, pollution, and habitat destruction 
        are threatening marine life and livelihoods that depend on the sea. Coastal communities face the challenge of preserving marine biodiversity while meeting the growing 
        demand for fish and seafood. Sustainable fishing practices, improved marine protected areas, and stricter enforcement of anti-pollution laws are essential for protecting 
        the country’s oceans and ensuring the long-term viability of marine resources.
    """,
    "Life on Land": """
        Deforestation, illegal logging, and land conversion continue to degrade the Philippines’ rich terrestrial ecosystems. These environmental issues not only threaten biodiversity 
        but also contribute to climate change and natural disasters like floods and landslides. The government has implemented policies such as the National Integrated Protected Areas 
        System (NIPAS) Act to protect forest lands and wildlife, but enforcement remains a challenge. Addressing land degradation requires a combination of conservation efforts, 
        sustainable land use practices, and community-based environmental stewardship.
    """,
    "Peace, Justice, and Strong Institutions": """
        The Philippines faces challenges related to corruption, human rights abuses, and weak rule of law. Strengthening institutions to promote peace, justice, and good governance is 
        critical for the country’s long-term development. The government has introduced anti-corruption measures and legal reforms, but more work is needed to ensure accountability, 
        transparency, and access to justice for all. Enhancing civil society participation, protecting human rights, and strengthening the independence of the judiciary are key to 
        building a just society.
    """,
    "Partnerships for the Goals": """
        Achieving the SDGs requires cooperation between governments, businesses, civil society, and citizens. In the Philippines, partnerships are essential to address issues such as poverty, 
        inequality, and climate change. Multi-stakeholder partnerships can drive innovation, mobilize resources, and scale up solutions to complex problems. Strengthening the role of the private 
        sector, fostering international cooperation, and encouraging public-private partnerships are vital for achieving the SDGs by 2030.
    """

}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'sdgData.json')) as f:
    sdg_data = json.load(f)

with open(os.path.join(BASE_DIR, 'text.json')) as f:
    sdg_p = json.load(f)

@app.route('/')
def home():
    return render_template('index.html', sdg_titles=sdg_titles)

@app.route('/sdg/<int:sdg_number>')
def show_sdg(sdg_number):
    if 1 <= sdg_number <= len(sdg_titles):
        sdg_title = sdg_titles[sdg_number - 1]
        paragraph = sdg_paragraphs.get(sdg_title, "No detailed description available.")
        print(sdg_number)
        return render_template('sdg_detail.html', 
                            sdg_number=sdg_number,
                            sdg_title=sdg_title,
                            paragraph=paragraph)
    return "SDG not found", 404
@app.route('/api/sdg/<sdg_number>')
def pass_sdg(sdg_number):

    if sdg_number in sdg_data:
        return jsonify(sdg_data[sdg_number])
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/api/sdg_par/<sdg_number>')
def pass_par(sdg_number):

    if sdg_number in sdg_data:
        return jsonify(sdg_p[sdg_number])
    else:
        return jsonify({'error': 'Not found'}), 404

@app.route('/news')
def news_sdg():
    return render_template('news.html')

@app.route('/api/test')
def api_test():
    test_url = "https://jsonplaceholder.typicode.com/posts/1"
    try:
        response = requests.get(test_url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/api/news')
def api_news():
    url = f"https://newsapi.org/v2/everything?q=philippines%20sustainable%20development&language=en&sortBy=publishedAt&apiKey={news_api}"
    print("Requesting URL:", url)
    
    response = requests.get(url)
    print("NewsAPI status code:", response.status_code)
    print("NewsAPI response text:", response.text)
    
    if response.status_code == 200:
        data = response.json()
        filtered_articles = []
        for article in data.get('articles', []):
            if 'philippines' in article['title'].lower() or \
               'philippines' in article['description'].lower() or \
               'philippines' in article['content'].lower():
                filtered_articles.append(article)
        articles = filtered_articles[:5]
        return jsonify(articles)
    else:
        return jsonify({'error': 'Failed to retrieve data'}), 500



if __name__ == "__main__":
    app.run(debug=False)
