import streamlit as st
import pandas as pd
from operations import preprocess_data, load_model

st.set_page_config(page_title='COVID-19 Strain Analysis Prediction', layout='wide', initial_sidebar_state='collapsed')
st.title('COVID-19 Strain Analysis Prediction')
# Custom styles
st.markdown("""
<style>
/* Center the title and add underline */
h1 {
    text-align: center;
    border-bottom: 2px solid #4CAF50;
    padding-bottom: 10px;
    margin-bottom: 50px;
}

/* Style for the upload button and file uploader */
.stFileUploader {
    margin: auto;
    width: 50%;
    border-color: #4CAF50;
}

button {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    font-size: 16px;
    cursor: pointer;
}

button:hover, .css-2trqyj:hover {
    background-color: #45a049; /* Darker green background on hover */
}
</style>
""", unsafe_allow_html=True)

st.subheader('Upload your Spectrum File')
uploaded_file = st.file_uploader("Choose a spectrum file (.txt)", type="txt")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, delimiter='\t', header=None, names=['wavelength', 'intensity'])
    st.line_chart(df.set_index('wavelength'))

    processed_data = preprocess_data(df)

    if processed_data is not None:
        # Button for predictions with the first model
        if st.button('Predict for COVID strain'):
            model = load_model('model.pkl')
            if model:
                prediction = model.predict(processed_data.reshape(1, -1))
                st.success(f'Strain is: {prediction}')
            else:
                st.error('Failed to load the model.')

        # Button for predictions with the second model
        if st.button('Predict with Omicron Substrain'):
            model_1 = load_model('model_1.pkl')
            if model_1:
                prediction = model_1.predict(processed_data.reshape(1, -1))
                st.success(f'Substrain is: {prediction}')
            else:
                st.error('Failed to load model 1.')


st.markdown("""
<div class="center-text">
    <h2>COVID-19 Variants Overview</h2>
    <p>The COVID-19 pandemic has been marked by the emergence of several variants of the virus SARS-CoV-2, each with distinct characteristics and impacts on public health measures, vaccine efficacy, and the course of the pandemic. Among these, the Delta, Kappa, Omicron, and the original strain (often referred to as the "wild type") have been significant. Here's an overview of each:</p>
    <ul>
        <li><b>Wild Type (Original Strain)</b>
            <ul>
                <li><b>Discovery:</b> The wild type refers to the original strain of SARS-CoV-2 identified in Wuhan, China, in December 2019.</li>
                <li><b>Characteristics:</b> As the first strain to spread globally, it set the baseline for the virus's genetic characteristics and behavior.</li>
                <li><b>Impact:</b> It was responsible for the initial wave of the pandemic, leading to worldwide lockdowns, significant morbidity and mortality, and the rapid development of vaccines aimed at its spike protein.</li>
            </ul>
        </li>
        <li><b>Delta Variant (B.1.617.2)</b>
            <ul>
                <li><b>Discovery:</b> First identified in India in late 2020.</li>
                <li><b>Characteristics:</b> The Delta variant showed increased transmissibility and a higher rate of hospitalizations compared to earlier strains. It also had some ability to evade immunity from previous infection or vaccination, though vaccines remained generally effective against severe disease.</li>
                <li><b>Impact:</b> Delta became the dominant strain globally by mid-2021, leading to surges in cases, hospitalizations, and deaths, even in populations with high vaccination rates.</li>
            </ul>
        </li>
        <li><b>Kappa Variant (B.1.617.1)</b>
            <ul>
                <li><b>Discovery:</b> Also first detected in India around the same time as the Delta variant.</li>
                <li><b>Characteristics:</b> Part of the same lineage as Delta but considered less transmissible and less severe in terms of disease outcomes.</li>
                <li><b>Impact:</b> While it did spread to various countries, it did not become as dominant or as concerning as the Delta variant, largely overshadowed by Delta's rapid spread and higher impact.</li>
            </ul>
        </li>
        <li><b>Omicron Variant (B.1.1.529)</b>
            <ul>
                <li><b>Discovery:</b> First reported to the World Health Organization from South Africa in November 2021.</li>
                <li><b>Characteristics:</b> Marked by an exceptionally high number of mutations, particularly on the spike protein, Omicron exhibited significant immune evasion capabilities, leading to reinfections and breakthrough infections in vaccinated individuals. However, infections were generally less severe compared to Delta, especially among the vaccinated.</li>
                <li><b>Impact:</b> Omicron led to record-breaking surges in COVID-19 cases worldwide due to its high transmissibility. It spurred a wave of booster vaccination campaigns aimed at bolstering protection against infection and severe disease.</li>
            </ul>
        </li>
    </ul>
    <p>Each of these variants has underscored the importance of genomic surveillance, vaccination, and public health readiness in responding to an evolving virus. The emergence of variants like Delta and Omicron also highlighted the need for global cooperation in vaccine distribution to prevent the spread and mutation of the virus.</p>
</div>
""", unsafe_allow_html=True)
