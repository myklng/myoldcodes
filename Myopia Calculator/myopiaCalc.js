//Rate of progression compared to Myopia
const myopiaRateHigh = 1.25;
const myopiaRate = 1;
const myopiaRateLow = 0.75;
const stellestRate = 1-0.66;
const miyoSmartRate = 1-0.6;
const myoVisionRate = 1-0.4;
const orthoKRate = 1-0.8;
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


var myopiaHigh = {
  backgroundColor: 'rgba(255,0,0,0.2)',
  borderColor: 'rgba(255,0,0,0.3)',
  fill: fillData.myopiaHigh,
  borderDash: [5,5],
  borderWidth: 1,
  pointRadius: 0,
  pointHitRadius: 0,
  label:"无防控(高)",
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
  label:"无防控(低)",
  data: []
};
var myopia = {
  label: "无防控",
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
  label: "依视路星趣控",
  data: []
};
var miyoSmart = {
  hidden: true,
  backgroundColor: 'rgba(255,200,0,1)',
  borderColor: 'rgba(255,200,0,1)',
  fill: fillData.miyoSmart,
  pointRadius: 2,
  label: "豪雅新乐学",
  data: []
};
var myoVision = {
  hidden: true,
  backgroundColor: 'rgba(20,30,140,1)',
  borderColor: 'rgba(20,30,140,1)',
  fill: fillData.myoVision,
  pointRadius: 2,
  label: "蔡司成长乐",
  data: []
};
var orthoK = {
  hidden: true,
  backgroundColor: 'rgba(0,200,200,1)',
  borderColor: 'rgba(0,200,200,1)',
  fill: fillData.orthoK,
  pointRadius: 2,
  label: "角膜塑形镜",
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
            return context[0].label+"岁";
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


//calculates projected Rx with ageArray n retuens dataset
function projectRx(currentRx, ageArray, rate, dataset) {
  //clear previous data
  dataset.data = [];
  let newRx = currentRx;
  ageArray.forEach((i) => {
    dataset.data.push(newRx.toFixed(2));
    if (i < 15) {
      newRx = newRx - (1*rate);
    }
    else if (i < 20) {
      newRx = newRx - (0.75*rate);
    }
    else {
      newRx = newRx - (0.50*rate);
    }
  });
  return dataset;
}

//calculates projected Rx n populates dataset from now till 24yo
function calcMyopia(currentAge, currentRx, maxAge) {
  //populate ages (X AXis) & highMyopia;
  let highMyopia = {
    borderColor: 'rgba(0,0,0,1)',
    backgroundColor: 'rgba(0,0,0,0)',
    fill: false,
    borderDash: [10,4],
    borderWidth: 1,
    pointRadius: 0,
    pointHitRadius: 0,
    label:"高度近视",
    data: []
  };
  ages = [];
  for (let i = 0; i <= maxAge; i++) {
    ages.push(i);
    highMyopia.data.push(-5.00);
  }
  //console.log("ages Array[]: "+ages)
  ages = ages.slice(currentAge)
  // async () => {
  //   let myopiaHigh = await projectRx(currentRx, ages, myopiaRateHigh, myopiaSD)
  //   .then(console.log("myopiaHigh "+myopiaHigh.data))
  //   .then(()=>{
  //     myopiaLow = projectRx(currentRx, ages, myopiaRateLow, myopiaSD);
  //     console.log("myopiaLow "+myopiaLow.data);
  //     console.log("myopiaHigh "+myopiaHigh.data);
  //   })
  // }
  myopiaHigh = projectRx(currentRx, ages, myopiaRateHigh, myopiaHigh);
  myopiaLow = projectRx(currentRx, ages, myopiaRateLow, myopiaLow);
  myopia = projectRx(currentRx, ages, myopiaRate, myopia);
  myoVision = projectRx(currentRx, ages, myoVisionRate, myoVision);
  miyoSmart = projectRx(currentRx, ages, miyoSmartRate, miyoSmart);
  stellest = projectRx(currentRx, ages, stellestRate, stellest);
  orthoK = projectRx(currentRx, ages, orthoKRate, orthoK);

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
