import fetch from 'isomorphic-fetch'

const endpoint = '/api/'

const parseJSON = response => {
  return new Promise(resolve => response.json()
    .then(json => resolve({
      status: response.status,
      ok: response.ok,
      json,
    })))
}

const request = (url, options = {}) => {

  options.headers = Object.assign({}, options.headers, {
    'Content-Type': 'application/json'
  })

  return new Promise((resolve, reject) => {
    fetch(endpoint + url, options)
      .then(parseJSON)
      .then(response => {
        if (response.ok) {
          return resolve(response.json)
        }
        return reject(response.json.message)
      })
      .catch(err => reject({
        networkError: err.error,
      }))
  })
}

export default request
