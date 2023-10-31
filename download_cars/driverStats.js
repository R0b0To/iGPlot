const separator = '	'
const tier = 'elite'
const leagueType = document.getElementById(tier).querySelector('h2').textContent.split('/')[1]
const table = document.querySelector(`#${tier} > table > tbody`);
let csv=`Manager${separator}Driver${separator}Livery${separator}Talent${separator}Grade${separator}Special${separator}Rating${separator}FavTrack${separator}Height${separator}BMI\n`;
for (var i = 0; i < table.rows.length; i++) {
    managerID = table.rows[i].childNodes[1].childNodes[1].href.match(/\d+/)[0];
    manager = table.rows[i].childNodes[1].childNodes[3].textContent.substring(1);
    managerData = await fetch("https://igpmanager.com/index.php?action=fetch&d=profile&manager="+managerID+"&csrfName=&csrfToken=")
    .then(response => response.json())
    .then(data => {return data})
    
    driverId = {};
    driverId.d1 = /\d+/.exec(managerData.vars.driver1)[0];
    if(leagueType == 16)
    {
      driverId.d2 = /\d+/.exec(managerData.vars.driver2)[0];
    }
    for(id in driverId)
    {
     driverData = await fetch(`https://igpmanager.com/index.php?action=fetch&d=driver&id=${driverId[id]}&csrfName=&csrfToken=`)
    .then(response => response.json())
    .then(data => {return data})
    driver = parseAttributes(driverData);
    bmiColor = /block-(.*)">/.exec(driverData.vars.sBmi)[1];
    livery = document.createElement("img");
    livery.innerHTML = managerData.vars.liveryS;
    imgLink = livery.childNodes[0].src;
    bmi ={"red":"❌","orange":"❎","green":"✅"};
    special={specialA0:"",specialA1:"Common",specialA2:"Rare",specialA3:"Legendary"}
    driverName = /\/>(.*)/.exec(driverData.vars.dName)[1];
    console.log("...")
    csv +=(`${manager}${separator}${driver.dName}${separator}${imgLink}${separator}${driver.sTalent}${separator}${special[driver.sSpecial.grade]}${separator}${driver.sSpecial.name}${separator}${driver.starRating}${separator}${driver.favTrack}${separator}${driver.sHeight}${separator}${bmi[driver.sBmi]}\n`);
    }
    
  }
console.log(csv);
copyToClipboard(csv)

function parseAttributes(personData) {
  function toCentimeters(height) {
    // Set up an object containing the conversion factors for feet and inches to centimeters
    const units = {ft: 30.48, in: 2.54, cm: 100 };
    // Check if the height value is in feet and inches or in centimeters
    let valueInCentimeters;
    if (height[1] == '\'') // If the height is in feet and inches, split the value into feet and inches
    {
      const [feet, inches] = height.split(' ');
      // Convert the feet and inches to centimeters and add them together
      valueInCentimeters = ((parseInt(feet) * units.ft)) + (parseInt(inches) * units.in);
    }
    else if (height[1] == '.')
      valueInCentimeters = parseFloat(height) * units.cm; // If the height is in meters
    else
      valueInCentimeters = parseInt(height) ; // If the height is in cm
    return valueInCentimeters;
  }
  function createHTMLElement(varName) {
    const fragmentToParse = document.createElement('table');
    fragmentToParse.innerHTML = personData.vars[varName];
    return fragmentToParse;
  }
  const dName = createHTMLElement('dName').textContent.slice(1); //removing extra space
  const favTrack = createHTMLElement('favTrack').textContent.slice(1);
  const sTalent = createHTMLElement('sTalent').textContent;
  const sHeight = toCentimeters(personData.vars.sHeight);
  const starRating = /\d+/.exec(personData.vars.starRating);
  const sBmi = createHTMLElement('sBmi').querySelector('span').classList[1].split('-')[1];
  const tName = createHTMLElement('tName').textContent;
  const tLink = createHTMLElement('tName').querySelector('a')?.href || null;
  const skill = createHTMLElement('sSpecial').querySelector('span')?.textContent || null;
  const gradeId = createHTMLElement('sSpecial').querySelector('span')?.classList[0] || null;
  const sSpecial = { name: skill, grade: gradeId };
  return { dName, favTrack, sTalent, sHeight, starRating, sBmi, tName, tLink, sSpecial };
}
function copyToClipboard(str) {
  console.log('\n\nClick anywhere on the page to copy the results above ↑')
  document.addEventListener('click',copy);
  function copy(){
    navigator.clipboard.writeText(str)
    .then(() => {
      console.log('Text copied to clipboard');
      document.removeEventListener('click',copy);
    })
    .catch((err) => {
      console.error('Could not copy text: ', err);
    });
  }
}