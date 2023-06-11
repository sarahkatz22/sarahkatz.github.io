function getSoup(url) {
    // Create a Beautiful Soup object from a URL to parse its HTML content
    // Returns the soup object
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, false);
    xhr.send();
    var soup = new DOMParser().parseFromString(xhr.responseText, "text/html");
    return soup;
}

function findMatchingProduct(targetProduct, productList, threshold) {
    // Finds the best matching product to the target product name from a given product list,
    // based on the FuzzyWuzzy algorithm, using a given threshold
    var bestMatch = null;
    var bestRatio = 0;

    for (var i = 0; i < productList.length; i++) {
        var ratio = fuzz.ratio(targetProduct.toLowerCase(), productList[i].toLowerCase());
        if (ratio > bestRatio) {
            bestRatio = ratio;
            bestMatch = productList[i];
        }
    }

    // Check if a suitable match is found
    if (bestMatch === null || bestRatio < threshold) {
        return null;
    } else {
        return bestMatch;
    }
}

function productComparison(soup1, soup2) {
    var products1 = soup1.querySelectorAll('article');
    var products2 = soup2.querySelector('.grid-uniform.grid-link__container');

    var dict1 = {};

    for (var i = 0; i < products1.length; i++) {
        var title1 = products1[i].querySelector('.h3.product-title').textContent.trim();
        var price1 = products1[i].querySelector('.price').textContent.trim();
        dict1[title1.slice(0, -3)] = [price1.slice(1)];
    }

    var list2 = [];
    var dict2 = {};

    var product2Items = products2.querySelectorAll('.grid__item.wide--one-fifth.large--one-quarter.medium-down--one-half');
    for (var j = 0; j < product2Items.length; j++) {
        var title2 = product2Items[j].querySelector('.grid-link__title');
        var title2Text = title2.textContent.trim();
        list2.push(title2Text);

        var price2 = product2Items[j].querySelector('.grid-link__meta');
        var price2Text = price2.childNodes[price2.childNodes.length - 1].textContent.trim();

        dict2[title2Text] = price2Text.slice(2);
    }

    for (var key in dict1) {
        if (dict1.hasOwnProperty(key)) {
            var match = findMatchingProduct(key, list2, 0.605);
            if (match !== null) {
                dict1[key].push(dict2[match]);
            }
        }
    }

    return dict1;
}

function strToFloat(dict) {
    var newDict = {};
    for (var key in dict) {
        if (dict.hasOwnProperty(key)) {
            var val = dict[key];
            var nVal = val.map(function(item) {
                return item.replace(/,/g, '');
            });
            var lNum = nVal.map(function(item) {
                return parseFloat(item);
            });
            newDict[key] = lNum;
        }
    }

    return newDict;
}

function atRisk(soup1, soup2) {
    var riskProducts = [];

    var d1 = productComparison(soup1, soup2);
    var nDict = strToFloat(d1);

    for (var key in nDict) {
        if (nDict.hasOwnProperty(key)) {
            var val = nDict[key];
            if (val.length > 1 && val[0] > val[1]) {
                riskProducts.push(key);
            }
        }
    }

    return riskProducts;
}

function safe(soup1, soup2) {
    var safeProducts = [];

    var d1 = productComparison(soup1, soup2);
    var nDict = strToFloat(d1);

    for (var key in nDict) {
        if (nDict.hasOwnProperty(key)) {
            var val = nDict[key];
            if (val.length > 1 && val[1] >= val[0]) {
                safeProducts.push(key);
            }
        }
    }

    return safeProducts;
}


function submitForm() {
    
    var value1 = document.getElementById('value1').value;
    var value2 = document.getElementById('value2').value;
    
    var soup1 = getSoup(value1);
    var soup2 = getSoup(value2);
    
    var riskProducts = atRisk(soup1, soup2);
    var safeProducts = safe(soup1, soup2);
    
    var resultElement = document.getElementById('result');
    resultElement.innerHTML = "Safe Products: " + safeProducts.join(", ") + "<br><br>At Risk Products: " + atRiskProducts.join(", ");
    
}
