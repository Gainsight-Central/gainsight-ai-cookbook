// Counts page views and the plugin download dialog opening.
// Each event is one row in the "Cookbook events" Google Form: event, page, referrer, session.
// No cookies and no personal data. The session is a random ID kept in sessionStorage for one tab.
(function () {
  // Skip local files and localhost so testing does not pollute the numbers. Skip automated browsers.
  if (location.protocol !== "https:" || navigator.webdriver) return;

  var FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeoCIwOlNsxtvbSEac99NgnBNxpuqX7P3oyJwz1ZNulMEKEwA/formResponse";
  var FIELDS = {
    event: "entry.510684786",
    page: "entry.777111127",
    referrer: "entry.1024441607",
    session: "entry.1290550501"
  };

  var session = "";
  try {
    session = sessionStorage.getItem("cookbook_session") || "";
    if (!session) {
      session = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
      sessionStorage.setItem("cookbook_session", session);
    }
  } catch (error) {
    session = "no-storage";
  }

  function track(eventName) {
    try {
      var data = new FormData();
      data.append(FIELDS.event, eventName);
      data.append(FIELDS.page, location.pathname);
      data.append(FIELDS.referrer, (document.referrer || "").slice(0, 300));
      data.append(FIELDS.session, session);
      // no-cors hides the response. A blocked or failed post is ignored.
      fetch(FORM, { method: "POST", mode: "no-cors", body: data, keepalive: true }).catch(function () {});
    } catch (error) {
      return;
    }
  }

  window.cookbookTrack = track;
  track("page_view");
})();
