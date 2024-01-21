var separator = '	'
var tier = 'elite'
var leagueType = parseInt(document.getElementById(tier).querySelector('h2').textContent.split('/')[1])
var table = document.querySelector(`#${tier} > table > tbody`);
var csv=`Team${separator}Manager${separator}Driver${separator}Livery${separator}Talent${separator}Grade${separator}Special${separator}Rating${separator}FavTrack${separator}Height${separator}BMI${separator}Color\n`;

async function fetchManager(manager){
  const response = await fetch(`https://igpmanager.com/index.php?action=fetch&d=profile&manager=${manager.id}&csrfName=&csrfToken=`)
  return await response.json()
}
const managers = [];
for (var i = 0; i < table.rows.length; i++) {
  const match = /#([0-9A-Fa-f]{3,6})\b/.exec(table.rows[i].firstChild.outerHTML);
  const color = match ? match[0] : "#000000";
  managers.push({team:table.rows[i].childNodes[1].childNodes[5].textContent,
                 color:color,
                 name:table.rows[i].childNodes[1].childNodes[3].textContent.substring(1),
                 id:table.rows[i].childNodes[1].childNodes[1].href.match(/\d+/)[0]});
}
Promise.all(
  managers.map(async (manager) => {
    const managerData = await fetchManager(manager);
    console.log('fetching',manager)
    const driverId = {};
    driverId.d1 = /\d+/.exec(managerData.vars.driver1)[0];
    if(leagueType == 16)
      driverId.d2 = /\d+/.exec(managerData.vars.driver2)[0];
    let stat =[];
    for(id in driverId)
    {
     const response = await fetch(`https://igpmanager.com/index.php?action=fetch&d=driver&id=${driverId[id]}&csrfName=&csrfToken=`)
     const driverData = await response.json()
     const driver = parseAttributes(driverData);
     const livery = document.createElement("img");
     livery.innerHTML = managerData.vars.liveryS;
     const imgLink = livery.childNodes[0].src;
     const bmi ={"red":"❌","orange":"❎","green":"✅"};
     const special={specialA0:"",specialA1:"Common",specialA2:"Rare",specialA3:"Legendary"}
     const string =(`${manager.team}${separator}${manager.name}${separator}${driver.dName}${separator}${imgLink}${separator}${driver.sTalent}${separator}${special[driver.sSpecial.grade]}${separator}${driver.sSpecial.name}${separator}${driver.starRating}${separator}${driver.favTrack}${separator}${driver.sHeight}${separator}${bmi[driver.sBmi]}${separator}${manager.color}`);
     stat.push(string);
    }
    manager.stat = stat.join('\n ');
  }),
).then(()=>{
  const managerStats = managers.map(manager => manager.stat);
  csv += managerStats.join('\n ');
  console.log(csv);
  copyToClipboard(csv)}
  );

function parseAttributes(personData) {
  function toCentimeters(height) {
    // Set up an object containing the conversion factors for feet and inches to centimeters
    const units = {ft: 30.48, in: 2.54, cm: 100 };
    // Check if the height value is in feet and inches or in centimeters
    let valueInCentimeters;
    if (height[1] == '\'') // If the height is in feet and inches, split the value into feet and inches
    {
      const [feet, inches] = height.split(' ');
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