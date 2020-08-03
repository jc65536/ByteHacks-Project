<template>
  <div style="display: flex; flex-grow: 1; flex-direction: column; margin-bottom: 300px">
      <div style="margin-top: 40px; display: flex; flex-direction: row; justify-content: space-between; align-items: center">
      <img src="https://upload.wikimedia.org/wikipedia/commons/b/bb/Editorial_cartoon_mocking_FDR%27s_%22Alphabet_agencies%22.jpg" style="width: 20%; display: inline-block"/>
      <div style="display: inline-block; width: 75%; height: 100%;">
        <p style="font-size: 3rem; font-weight: bold">What are the Alphabet Agencies?</p>
        <p style="font-size: 1.5rem">They may sound like confusing jargon, but they're important federal agencies that can help you through this difficult time! See the cards below for a brief description of what they do.</p>
      </div>
      </div>
      <table>
          <tr>
            <td class="card">
                <p class="acronym">AAA</p>
                <p class="subtitle">Agricultural Adjustment Association</p>
                <p class="description">Aims to reduce production of farm products in order to boost their prices.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Agricultural_Adjustment_Act">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">CCC</p>
                <p class="subtitle">Civil Conservation Corps</p>
                <p class="description">Employs Americans to build work projects, especially roads, bridges, and irrigation.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Civilian_Conservation_Corps">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">DRS</p>
                <p class="subtitle">Drought Relief Service</p>
                <p class="description">Purchases cattle to prevent starvation due to drought.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Drought_Relief_Service">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">SHD</p>
                <p class="subtitle">Subsistence Homesteads Division</p>
                <p class="description">Provides cheap plots of land to people to farm and provide for their own families.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Subsistence_Homesteads_Division">Learn more >>></a>
            </td>
          </tr>
          <tr>
            <td class="card">
                <p class="acronym">FCA</p>
                <p class="subtitle">Farm Credit Administration</p>
                <p class="description">Helps farmers to with their mortgages and lends money to struggling farms.</p>
                <a class="card-link" href="https://www.fca.gov/">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">FERA</p>
                <p class="subtitle">Federal Emergency Relief Administration</p>
                <p class="description">Provides labor jobs in local and state government.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Federal_Emergency_Relief_Administration">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">FWA</p>
                <p class="subtitle">Federal Works Agency</p>
                <p class="description">Employs Americans to build work projects, especially parks and water treatment centers.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Federal_Works_Agency">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">HOLC</p>
                <p class="subtitle">Home Owners’ Loan Corporation</p>
                <p class="description">Provides loans to homeowners who cannot pay their mortgage to prevent foreclosure.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Home_Owners%27_Loan_Corporation">Learn more >>></a>
            </td>
          </tr>
          <tr>
            <td class="card">
                <p class="acronym">NRA</p>
                <p class="subtitle">National Recovery Association</p>
                <p class="description">Sets prices and business codes in order to make the market more stable.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/National_Recovery_Administration">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">NYA</p>
                <p class="subtitle">National Youth Administration</p>
                <p class="description">Provides work and education opportunities for youth between the ages of 16 and 25.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/National_Youth_Administration">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">PWA</p>
                <p class="subtitle">Public Works Association</p>
                <p class="description">Employs Americans to build large-scale public works such as hospitals and schools.</p>
                <a class="card-link" href="https://www.apwa.net/">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">RA</p>
                <p class="subtitle">Resettlement Administration</p>
                <p class="description">Relocates struggling families to communities created by the federal government.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Resettlement_Administration">Learn more >>></a>
            </td>
          </tr>
          <tr>
            <td class="card">
                <p class="acronym">SSA</p>
                <p class="subtitle">Social Security Administration</p>
                <p class="description">Provides social benefits to working Americans, such as a guaranteed social insurance plan for retired workers over 65.</p>
                <a class="card-link" href="https://www.ssa.gov/">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">TVA</p>
                <p class="subtitle">Tennessee Valley Authority</p>
                <p class="description">Employs Americans to create public works that help with power generation, fertilizer manufacturing, flood control, and agriculture in Tennessee.</p>
                <a class="card-link" href="https://www.tva.com/">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">USHA</p>
                <p class="subtitle">United States Housing Authority</p>
                <p class="description">Creates public housing for low-income and homeless Americans.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/United_States_Housing_Authority">Learn more >>></a>
            </td>
            <td class="card">
                <p class="acronym">WPA</p>
                <p class="subtitle">Works Progress Administration</p>
                <p class="description">Employs Americans to carry out public works projects, such as parks, roads, dams, schools, and post offices.</p>
                <a class="card-link" href="https://en.wikipedia.org/wiki/Works_Progress_Administration">Learn more >>></a>
            </td>
          </tr>
      </table>
  </div>
</template>

<script>

export default {
  name: "Example",
  components: {
  },
  data() {
    return {
    };
  },
  methods: {
  },
  mounted() {
  },
};

</script>

<style scoped>
table {
    margin: auto;
    border-collapse: separate;
    border-spacing: 15px;
    margin-top: 20px;
}

.card {
  padding: 10px;
  margin: 10px 0px;
  border-radius: 10px;
  box-shadow: 0px 1px 3px 0px #333;
  width: 300px;
  height: 300px;
  text-align: center;
  position: relative;
  vertical-align: top;
}

.card:hover {
    box-shadow: 0px 2px 6px 0px #333;
    transition: box-shadow 0.2s;
}

.acronym {
    margin-top: 5%;
    font-size: 2rem;
    font-weight: bold;
}

.subtitle {
    font-style: italic;
}

.description {
    position: absolute;
    width: 80%;
    left: 50%;
    top: 50%;
    transform: translateX(-50%) translateY(-50%);
}

.card-link {
    display: block;
    position: absolute;
    bottom: 10%;
    left: 50%;
    transform: translateX(-50%);
    text-decoration: underline;
    color: #2b67cd;
    padding: 5px 10px;
}

.card-link:hover {
    background-color: rgba(43, 103, 205, 0.1);
    transition: background-color 0.2s;
}

.collapsing {
  height: auto;
  max-height: 0px;
  transition: max-height 0.2s cubic-bezier(0.1, 1.1, 0.5, 0.95);
}

.expanding {
  height: auto;
  max-height: 50px;
  transition: max-height 0.2s cubic-bezier(0.1, 1.1, 0.5, 0.95);
}
</style>