"""Streamlit frontend for Travel Planning with OpenAI and Enuygun."""
import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import openai
from typing import Dict, Any
import re

# API endpoint
API_URL = "http://localhost:8000/chat"

# OpenAI API Key
OPENAI_API_KEY = "sk-proj-MBcp7esOGI0SgdHASpTliDW\nNxbf7xR38yoALTjXmVmoZqNH9W4aC\nVZNeWCAnJwTzQBuezBqMART3BlbkF\nJANQlG_tGLm1zwYKPXZIKl2lEx8QntH\nJZvV5UQMRgr_NR-dFNV2ZXa8wf-cE6\nwjI_fr4qs14hEA"

# OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY.replace("\n", ""))

def extract_travel_info_with_llm(message: str, travel_info: Dict[str, Any], conversation_history: list) -> tuple:
    """
    LLM kullanarak seyahat bilgilerini çıkarır ve yanıt oluşturur.
    
    Returns:
        tuple: (güncellenmiş_travel_info, asistan_yanıtı)
    """
    try:
        # Konuşma geçmişini hazırla
        messages = [
            {
                "role": "system",
                "content": """Sen bir seyahat planlama asistanısın. Kullanıcıdan seyahat bilgilerini topluyorsun.

Gerekli bilgiler:
- start_city: Başlangıç şehri
- destination_city: Varış şehri
- date: Gidiş tarihi (YYYY-MM-DD formatında)
- duration: Kalış süresi (gün sayısı olarak)
- transport_type: Ulaşım türü (Uçak veya Otobüs)

Şu anki bilgiler: """ + json.dumps(travel_info, ensure_ascii=False) + """

Görevin:
1. Kullanıcının mesajından yukarıdaki bilgileri çıkar
2. Eksik bilgiler varsa, doğal bir şekilde sor
3. Tüm bilgiler tamamsa, özet göster ve onay iste
4. Yanıtını JSON formatında ver:

{
  "travel_info": {
    "start_city": "...",
    "destination_city": "...",
    "date": "YYYY-MM-DD",
    "duration": sayı,
    "transport_type": "Uçak" veya "Otobüs"
  },
  "response": "Kullanıcıya verilecek yanıt mesajı",
  "is_complete": true/false
}

SADECE JSON yanıtı ver, başka bir şey yazma."""
            }
        ]
        
        # Konuşma geçmişini ekle
        messages.extend(conversation_history[-6:])  # Son 3 mesaj çifti
        
        # Yeni kullanıcı mesajını ekle
        messages.append({"role": "user", "content": message})
        
        # LLM'e gönder
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        # Yanıtı parse et
        result = json.loads(response.choices[0].message.content)
        
        # Seyahat bilgilerini güncelle
        if "travel_info" in result:
            for key, value in result["travel_info"].items():
                if value:  # Sadece değer varsa güncelle
                    travel_info[key] = value
        
        return travel_info, result.get("response", "Devam edelim."), result.get("is_complete", False)
        
    except Exception as e:
        st.error(f"LLM hatası: {str(e)}")
        # Hata durumunda basit bir yanıt dön
        return travel_info, "Bir hata oluştu. Lütfen tekrar deneyin.", False

def get_travel_recommendations(travel_info: Dict[str, Any]) -> str:
    """
    Get travel recommendations from OpenAI.
    
    Args:
        travel_info: Travel information dictionary
        
    Returns:
        Travel recommendations
    """
    try:
        prompt = f"""Lütfen aşağıdaki seyahat bilgileri için detaylı bir gezi planı oluştur:

- Gidilecek Şehir: {travel_info['destination_city']}
- Kalış Süresi: {travel_info['duration']} gün

Lütfen şunları içeren bir plan hazırla:
1. Günlük gezilecek yerler ve aktiviteler
2. Yemek önerileri
3. Dikkat edilmesi gereken noktalar
4. Tahmini bütçe
"""

        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir seyahat danışmanısın. Türkçe yanıt ver."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"OpenAI API hatası: {str(e)}")
        return "Üzgünüm, gezi planı oluşturulurken bir hata oluştu."

def get_enuygun_recommendations(travel_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get travel recommendations from Enuygun MCP.
    
    Args:
        travel_info: Travel information dictionary
        
    Returns:
        Enuygun recommendations
    """
    try:
        response = requests.post(
            API_URL,
            json={
                "message": f"Lütfen {travel_info['start_city']}'den {travel_info['destination_city']}'e {travel_info['date']} tarihinde {travel_info['transport_type']} ile seyahat önerileri göster",
                "clear_history": False
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Enuygun API hatası: {str(e)}")
        return {"response": "Üzgünüm, seyahat önerileri alınırken bir hata oluştu."}

def main():
    """Main Streamlit application."""
    # Sayfa başlığı ve açıklama
    st.set_page_config(
        page_title="Seyahat Planlayıcı",
        page_icon="✈️",
        layout="centered"
    )
    
    # Başlık
    st.title("✈️ Akıllı Seyahat Planlayıcı")
    st.markdown("""
    Bu uygulama, OpenAI ve Enuygun entegrasyonu ile size özel seyahat planları oluşturur.
    Benimle sohbet ederek seyahat planınızı oluşturalım!
    """)

    # Session state başlangıç değerleri
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.travel_info = {}
        st.session_state.is_complete = False
        initial_message = "Merhaba! Size nasıl yardımcı olabilirim? Seyahat planınızı anlatın, ben gerekli bilgileri not alacağım."
        st.session_state.messages.append({"role": "assistant", "content": initial_message})

    # Geçmiş mesajları göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Kullanıcı girişi
    user_input = st.chat_input("Mesajınızı yazın...")

    if user_input:
        # Kullanıcı mesajını göster ve kaydet
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        # LLM ile mesajı işle ve bilgileri çıkar
        with st.spinner("Düşünüyorum..."):
            updated_info, assistant_response, is_complete = extract_travel_info_with_llm(
                user_input, 
                st.session_state.travel_info,
                st.session_state.messages
            )
            st.session_state.travel_info = updated_info
            st.session_state.is_complete = is_complete

        # Asistan yanıtını göster ve kaydet
        with st.chat_message("assistant"):
            if not is_complete:
                # Henüz tüm bilgiler toplanmadı
                st.write(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                # Tüm bilgiler toplandı, sonuçları göster
                st.write(assistant_response)
                st.write("\n**Toplanan Bilgiler:**")
                st.write(f"""
                - Başlangıç şehri: {st.session_state.travel_info.get('start_city', 'Belirtilmedi')}
                - Gidilecek şehir: {st.session_state.travel_info.get('destination_city', 'Belirtilmedi')}
                - Gidiş tarihi: {st.session_state.travel_info.get('date', 'Belirtilmedi')}
                - Kalış süresi: {st.session_state.travel_info.get('duration', 'Belirtilmedi')} gün
                - Ulaşım türü: {st.session_state.travel_info.get('transport_type', 'Belirtilmedi')}
                """)

                # Sonuçları göster
                st.markdown("### 🎫 Ulaşım Önerileri")
                with st.spinner("Ulaşım önerileri alınıyor..."):
                    enuygun_recommendations = get_enuygun_recommendations(st.session_state.travel_info)
                    st.markdown(enuygun_recommendations["response"])
                
                st.markdown("### 📍 Gezi Planı")
                with st.spinner("Gezi planı oluşturuluyor..."):
                    travel_plan = get_travel_recommendations(st.session_state.travel_info)
                    st.markdown(travel_plan)
                
                # Sohbeti sıfırla
                st.session_state.is_complete = False

    # Yeni sohbet başlatma butonu
    if st.sidebar.button("Yeni Sohbet Başlat"):
        st.session_state.messages = []
        st.session_state.travel_info = {}
        st.rerun()

if __name__ == "__main__":
    main()