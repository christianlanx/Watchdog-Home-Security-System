/**
 * Name: Joseph Chao
 * Date: 10/29
 * Section: CSE 154 AJ, Lauren Krieger
 *
 * -- your description of what this file does here --
 * Do not keep comments from this template in any work you submit (functions included under "Helper
 * functions" are an exception, you may keep the function names/comments of id/qs/qsa/gen)
 */
 "use strict";

 (function() {

    window.addEventListener("load", init);
    function init() {
        let tempBtn = id("temperature_button");
        let humBtn = id("humidity_button");
        let alarmBtn = id("alarm_button");
        let cameraBtn = id("camera_button");
        tempBtn.addEventListener("click", showTempGraph);
        humBtn.addEventListener("click", showHumGraph);
        cameraBtn.addEventListener("click", showCamVideo);
        //fetchData();
        displayCurrentNumber();
        //setInterval(reloadCurrent, 5000);
        //setInterval(reloadCurrent, 500000);
    }

    function reloadCurrent() {
        id("current_temp").src = id("current_temp").src;
        id("current_humd").src = id("current_humd").src;
    }

    function reloadGraph() {
        id("temp_frame").src = id("temp_frame").src;
        id("humd_frame").src = id("humd_frame").src;
        id("hardware_frame").src = id("hardware_frame").src;
    }

    function fetchData() {
        let url = "http://192.168.50.168/grafana/api/dashboards/id/1/permissions";

        fetch(url, {
            mode: 'no-cors',
            method: 'GET',
            Accept: "application/json",
            ContentType: "application/json",
            hideFromInspector: "false",
        })
          .then(checkStatus)
          .then(resp => resp.json())
          .then(processData)
          .catch(console.error);
    }

    function processData(tempJson) {
        console.log(tempJson.status);
    }

    function showTempGraph() {
        //window.location = "/grafana/d-solo/RyOmzRCMz/sensor-dashboard?orgId=1&from=1621286669920&to=1621373069920&panelId=10";
        let allGraphs = qsa("#dashboard div");
        for (let i = 0; i < allGraphs.length; i++) {
            allGraphs[i].classList.add("hidden");
        }
        let graph = id("temp_Graph");
        graph.classList.remove("hidden");
    }

    function showHumGraph() {
        //window.location = "/grafana/d-solo/RyOmzRCMz/sensor-dashboard?orgId=1&from=1621286683896&to=1621373083896&panelId=4";
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
    
