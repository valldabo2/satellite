const Http = {
  get: (url, options) => request(url, "GET", options),
  put: (url, options) => request(url, "PUT", options),
  post: (url, options) => request(url, "POST", options),
  delete: (url, options) => request(url, "DELETE", options),
  head: (url, options) => request(url, "HEAD", options)
};

const defaultJsonHeaders = {
  Accept: "application/json",
  "Content-Type": "application/json"
};

function request(url, method, options = {}) {
  const headers = new Headers(
    Object.assign({}, defaultJsonHeaders, options.headers)
  );

  const body = options.body && JSON.stringify(options.body);

  return fetch(url, Object.assign({}, options, { headers, method, body }))
    .then(checkStatus)
    .then(parseJSON);
}

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }
  const error = new HttpError(response);
  error.response = response;
  throw error;
}

function parseJSON(response) {
  if (response.status === 204 || response.status === 205) {
    return null;
  }

  if (response.headers.get("content-type").startsWith("text")) {
    return response.text();
  }

  return response.json();
}

export class HttpError extends Error {
  constructor({ url, status, statusText }) {
    super();
    this.message = `Request ${url} failed with '${statusText}'${status}`;
    this.status = status;
  }
}

export default Http;
