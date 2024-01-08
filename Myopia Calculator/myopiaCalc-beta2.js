//Citations to use Vancouver/NLM Style

//Rate of progression compared to Myopia
//Padmaja Sankaridurg, Brien A Holden, Leslie A Donovan, Chi-ho To, Wei Han Chua, Li Li, Xiang Chen; An Annual Rate of Myopic Progression Model for Asian children. Invest. Ophthalmol. Vis. Sci. 2014;55(13):3629.
//rate = -((0.0029*age)^2)+(0.145*age)-1.7784
//(for SPL: 6 yr: -1.02±0.41D; 10 yrs: -0.63±0.42; 13 yrs: -0.47±0.32D)
//myopiaRateTables Array by age [1yo,2yo etc]
const myopiaRateTableNormal = [-1.02,-1.02,-1.02,-1.02,-1.02,-1.02,-1.02,-1.02,-1.02,-1.02,-0.63,-0.63,-0.63,-0.47,-0.47,-0.47,-0.47,-0.47,-0.47,-0.47];
const myopiaRateTableLow = [-0.61,-0.61,-0.61,-0.61,-0.61,-0.61,-0.61,-0.61,-0.61,-0.61,-0.21,-0.21,-0.21,-0.15,-0.15,-0.15,-0.15,-0.15,-0.15,-0.15];
const myopiaRateTableHigh = [-1.43,-1.43,-1.43,-1.43,-1.43,-1.43,-1.43,-1.43,-1.43,-1.43,-1.05,-1.05,-1.05,-0.79,-0.79,-0.79,-0.79,-0.79,-0.79,-0.79];
const myopiaRateHigh = 1.25;
const myopiaRate = 1;
const myopiaRateLow = 0.75;

//Philip K. What’s New in Spectacle Lenses for Myopia Management? - Review of Myopia Management [Internet]. Review of Myopia Management. 2021 [cited 7 July 2021]. Available from: https://reviewofmm.com/whats-new-in-spectacle-lenses-for-myopia-management/
const stellestRate = 1-0.63;
const miyoSmartRate = 1-0.52;
const myoVisionRate = 1-0.154;

//Lee YC, Wang JH, Chiu CJ. Effect of orthokeratology on myopia progression: twelve-year results of a retrospective cohort study. BMC ophthalmology. 2017 Dec;17(1):1-8.
//Starting from OrthoK Year 0 onwards
const orthoKRateTable = [-0.17,-0.17,-0.23,-0.23,-0.28,-0.28,-0.32,-0.32,-0.23,-0.23,-0.06,-0.06,-0.06,-0.06,-0.06,-0.06,-0.06,-0.06,-0.06,-0.06]
const orthoKRate = 1; // follows orthoKRateTable

const fillData = {
  myopiaHigh: '+2',
  myopiaLow: false,
  myopia: false,
  //stellest: false,
  stellest: {
    target: '+1',
    above:'rgba(1,124,194,0.3)'
  },
  // miyoSmart: false,
  miyoSmart: {
    target: '+1',
    above:'rgba(255,200,0,0.3)'
  },
  // myoVision: false,
  myoVision: {
    target: '+1',
    above:'rgba(20,30,140,0.3)'
  },
  orthoK: false
}
const myoTranslations = {
  highMyopia: {
    en: "HighMyopia",
    cn: "高度近视",
    tw: "高度近視"
  },
  myopiaHigh: {
    en: "(High)",
    cn: "(高)",
    tw: "(高)"
  },
  myopiaLow: {
    en: "(Low)",
    cn: "(低)",
    tw: "(低)"
  },
  myopia: {
    en: "Std Gls/CLs",
    cn: "普通眼镜／隐眼",
    tw: "普通眼鏡／隱鏡"
  },
  stellest: {
    en: "ESS Stellest",
    cn: "依视路星趣控",
    tw: ""
  },
  miyoSmart: {
    en: "HOYA MiYOSART",
    cn: "豪雅新乐学",
    tw: ""
  },
  myoVision: {
    en: "CZ MyoVision",
    cn: "蔡司成长乐",
    tw: ""
  },
  orthoK: {
    en: "OrthoK",
    cn: "角膜塑形镜",
    tw: ""
  }
}
/*
myoConfig.options.scales.x.scaleLabel.labelString
myoConfig.options.scales.y.scaleLabel.labelString
myoConfig.options.plugins.title.text
*/

var highMyopia = {
  borderColor: 'rgba(0,0,0,1)',
  backgroundColor: 'rgba(0,0,0,0)',
  fill: false,
  borderDash: [10,4],
  borderWidth: 1,
  pointRadius: 0,
  pointHitRadius: 0,
  label:"",
  data: []
};
var myopiaHigh = {
  backgroundColor: 'rgba(255,0,0,0.2)',
  borderColor: 'rgba(255,0,0,0.3)',
  fill: fillData.myopiaHigh,
  borderDash: [5,5],
  borderWidth: 1,
  pointRadius: 0,
  pointHitRadius: 0,
  label: "",
  data: []
};
var myopiaLow = {
  backgroundColor: 'rgba(255,0,0,0.1)',
  borderColor: 'rgba(255,0,0,0.3)',
  fill: fillData.myopiaLow,
  borderDash: [5,5],
  borderWidth: 1,
  pointRadius: 0,
  pointHitRadius: 0,
  label: "",
  data: []
};
var myopia = {
  label: "",
  backgroundColor: 'rgba(255,0,0,1)',
  borderColor: 'rgba(255,0,0,1)',
  pointRadius: 2,
  fill: fillData.myopia,
  data: []
};
var stellest = {
  hidden: true,
  backgroundColor: 'rgba(1,124,194,1)',
  borderColor: 'rgba(1,124,194,1)',
  fill: fillData.stellest,
  pointRadius: 2,
  label: "",
  data: []
};
var miyoSmart = {
  hidden: true,
  backgroundColor: 'rgba(255,200,0,1)',
  borderColor: 'rgba(255,200,0,1)',
  fill: fillData.miyoSmart,
  pointRadius: 2,
  label: "",
  data: []
};
var myoVision = {
  hidden: true,
  backgroundColor: 'rgba(20,30,140,1)',
  borderColor: 'rgba(20,30,140,1)',
  fill: fillData.myoVision,
  pointRadius: 2,
  label: "",
  data: []
};
var orthoK = {
  hidden: true,
  backgroundColor: 'rgba(0,200,200,1)',
  borderColor: 'rgba(0,200,200,1)',
  fill: fillData.orthoK,
  pointRadius: 2,
  label: "",
  data: []
};
var ages = [];
var test;
var test2;
var myoConfig = {
  type: 'line',
  data: {
    //labels: [],
    datasets: []
  },
  options: {
    interaction: {
        mode: 'nearest',
        intersect: false
    },
    plugins:{
      tooltip:{
        enabled: true,
        displayColors: true,
        usePointStyle: false,
        filter: function(item) {
          return !item.label.includes('xxx');
        },
        callbacks: {
          labelColor: function(context) {
            test2 = context;
            return {
                        borderColor: 'rgba(255,255,255)',//context.dataset.borderColor,
                        backgroundColor: context.dataset.borderColor
                    };
          },
          label: function(context) {
            //test2 = context;
            return context.dataset.label+": "+parseFloat(context.formattedValue).toFixed(2);
          },
          title: function(context) {
            //test = context;
            //console.log(context.label);
            if ( currentLang == "zh-cn") {
              return context[0].label+"岁";
            } else if (currentLang == "zh-tw") {
              return context[0].label+"歲";
            } {
              return context[0].label+"YO";
            }
          },
        }
      },
      legend:{
        position: "top",
        // onHover: function(event, legendItem) {
        //   console.log(legendItem);
        // },
        labels: {
          filter: function(item) {
            return !item.text.includes('(');
          }
        }
      },
      title: {
        font: {size: 20},
        lineHeight: 1.5,
        display: true,
        color: 'rgba(0,0,0,1)',
        text: "Myopia Vs Myopia Control Calculator(近视与近视防控计算表)"
      }
    },
    aspectRatio: 1.61,
    scales: {
      x: {
        display: true,
        scaleLabel: {
          display: true,
            font: {size: 16},
          labelString: "Age(年龄)"
        },
        ticks: {
          beginAtZero: false
        }
      },
      y: {
        max: 0,
        display: true,
        reverse: true,
        scaleLabel: {
          display: true,
          font: {size: 16},
          labelString: "Myopia(近视)"
        },
        ticks: {
          beginAtZero: true,
          stepSize: 5
        }
      }
    }
  }
};


//calculates projected Rx with ageArray n returns dataset
function projectRx(currentRx, ageArray, rate, dataset, myopiaRate) {
  // myopiaRate refers to normal, low or high and which myopiaRateTable to use
  //clear previous data
  dataset.data = [];
  let rateTable = [];
  let newRx = currentRx;
  //calculate orthoKRatePerYear by combining myopiaRateTable with orthoKRateTable
  convertedOrthoKRateTable = myopiaRateTableNormal.slice(0,ageArray[0]);
  convertedOrthoKRateTable = convertedOrthoKRateTable.concat(orthoKRateTable);
  ageArray.forEach((i) => {
    dataset.data.push(newRx.toFixed(2));
    if (myopiaRate == 'orthoK') {
      rateTable = convertedOrthoKRateTable;
    } else if (myopiaRate == 'high') {
      rateTable = myopiaRateTableHigh;
    } else if (myopiaRate == 'low') {
      rateTable = myopiaRateTableLow;
    } else {
      rateTable = myopiaRateTableNormal;
    }
    newRx = newRx + (rateTable[i]*rate);
    // if (i < 15) {
    //   newRx = newRx - (1*rate);
    // }
    // else if (i < 20) {
    //   newRx = newRx - (0.75*rate);
    // }
    // else {
    //   newRx = newRx - (0.50*rate);
    // }
  });
  return dataset;
}

//calculates projected Rx n populates dataset from now till 24yo
function calcMyopia(currentAge, currentRx, maxAge) {
  //populate ages (X AXis) & highMyopia Line;
  ages = [];
  for (let i = 0; i <= maxAge; i++) {
    ages.push(i);
    highMyopia.data.push(-5.00);
  }
  //console.log("ages Array[]: "+ages)
  ages = ages.slice(currentAge)

  // update labels with Translations
  myoLang = "";
  if ( currentLang == "zh-cn") {
    myoLang = "cn";
  } else if (currentLang == "zh-tw") {
    myoLang = "tw";
  } else {
    myoLang = "en";
  }
  highMyopia.label = myoTranslations.highMyopia[myoLang];
  myopiaHigh.label = myoTranslations.myopiaHigh[myoLang];
  myopiaLow.label = myoTranslations.myopiaLow[myoLang];
  myopia.label = myoTranslations.myopia[myoLang];
  stellest.label = myoTranslations.stellest[myoLang];
  miyoSmart.label = myoTranslations.miyoSmart[myoLang];
  myoVision.label = myoTranslations.myoVision[myoLang];
  orthoK.label = myoTranslations.orthoK[myoLang];

  myopiaHigh = projectRx(currentRx, ages, myopiaRate, myopiaHigh, 'high');
  myopiaLow = projectRx(currentRx, ages, myopiaRate, myopiaLow, 'low');
  myopia = projectRx(currentRx, ages, myopiaRate, myopia, 'norm');
  myoVision = projectRx(currentRx, ages, myoVisionRate, myoVision, 'norm');
  miyoSmart = projectRx(currentRx, ages, miyoSmartRate, miyoSmart, 'norm');
  stellest = projectRx(currentRx, ages, stellestRate, stellest, 'norm');
  orthoK = projectRx(currentRx, ages, orthoKRate, orthoK, 'orthoK');

  myoConfig.data.labels = [];
  myoConfig.data.datasets = [];
  myoConfig.data.labels = ages;
  myoConfig.data.datasets.push(highMyopia);
  myoConfig.data.datasets.push(myopiaHigh);
  myoConfig.data.datasets.push(myopia);
  myoConfig.data.datasets.push(myopiaLow);
  myoConfig.data.datasets.push(myoVision);
  myoConfig.data.datasets.push(miyoSmart);
  myoConfig.data.datasets.push(stellest);
  myoConfig.data.datasets.push(orthoK);
  myoChart.update();
}

function makeMyopiaChart() {
  let age = parseFloat(document.getElementById('ageSelect').value);
  let rx = parseFloat(document.getElementById('rxSelect').value);
  let maxAge = parseFloat(document.getElementById('maxAgeSelect').value);
  calcMyopia(age, rx, maxAge)
}
