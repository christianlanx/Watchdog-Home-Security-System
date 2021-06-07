/**
 * Name: Joseph Chao
 * Date: 2021/6/7
 */
 "use strict";

 (function() {

    window.addEventListener("load", init);
    function init() {
        let tempBtn = id("temperature_button");
        let humBtn = id("humidity_button");
        let alarmBtn = id("alarm_button");
        let cameraBtn = id("camera_button");
        let noiseBtn = id("noise_button");
        let dashboardBtn = id("dashboard_button");
        tempBtn.addEventListener("click", showTempGraph);
        humBtn.addEventListener("click", showHumGraph);
        alarmBtn.addEventListener("click", showMotionGraph);
        cameraBtn.addEventListener("click", showCamVideo);
        dashboardBtn.addEventListener("click", showGraph);
        noiseBtn.addEventListener("click", showNoiseGraph);
        //fetchData();
        displayCurrentNumber();
        //setInterval(reloadCurrent, 5000);
        //setInterval(reloadCurrent, 500000);
    }

    function showGraph() {
        window.location = "/grafana/d/RyOmzRCMz/sensor-dashboard?orgId=1";
    }

    function showNoiseGraph() {
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("noise_Graph");
        graph.classList.remove("hidden");
    }

    function showTempGraph() {
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("temp_Graph");
        graph.classList.remove("hidden");
    }

    function showMotionGraph() {
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("motion_Graph");
        graph.classList.remove("hidden");
    }

    function showHumGraph() {
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("hum_Graph");
        graph.classList.remove("hidden");
    }

    function showCamVideo() {
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("cam_Video");
        graph.classList.remove("hidden");
    }

    function displayCurrentNumber() {
            let currentTime = Date.now();
            console.log(Math.floor(currentTime/10000)*10000);
    }


    /** ------------------------------ Helper Functions  ------------------------------ */
    /**
    * Note: You may use these in your code, but remember that your code should not have
    * unused functions. Remove this comment in your own code.
    */

        /**
     * Returns the element that has the ID attribute with the specified value.
     * @param {string} idName - element ID
     * @returns {object} DOM object associated with id.
     */
    function id(idName) {
        return document.getElementById(idName);
    }

    /**
     * Returns the first element that matches the given CSS selector.
     * @param {string} selector - CSS query selector.
     * @returns {object} The first DOM object matching the query.
     */
    function qs(selector) {
        return document.querySelector(selector);
    }

    /**
     * Returns the array of elements that match the given CSS selector.
     * @param {string} selector - CSS query selector
     * @returns {object[]} array of DOM objects matching the query.
     */
    function qsa(selector) {
        return document.querySelectorAll(selector);
    }

    /**
     * Returns a new element with the given tag name.
     * @param {string} tagName - HTML tag name for new DOM element.
     * @returns {object} New DOM object for given HTML tag.
     */
    function gen(tagName) {
        return document.createElement(tagName);
    }

    async function checkStatus(res) {
        if (!res.ok) {
          throw new Error(await res.text());
        }
        return res;
    }
})();
    
