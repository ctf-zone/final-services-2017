import request from './api'
import { toastr } from 'react-redux-toastr'
import queryString from 'query-string'

export const SHOW_MODAL = 'SHOW_MODAL'
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS'
export const SIGNUP_SUCCESS = 'SIGNUP_SUCCESS'
export const GET_USER_SUCCESS = 'GET_USER_SUCCESS'
export const LOGOUT = 'LOGOUT'
export const CREATE_PETITION_SUCCESS = 'CREATE_PETITION_SUCCESS'
export const GET_PETITIONS_SUCCESS = 'GET_PETITIONS_SUCCESS'
export const GET_PETITION_SUCCESS = 'GET_PETITION_SUCCESS'
export const SIGN_PETITION_SUCCESS = 'SIGN_PETITION_SUCCESS'
export const GET_SIGNERS_SUCCESS = 'GET_SIGNERS_SUCCESS'
export const GET_STATS_SUCCESS = 'GET_STATS_SUCCESS'
export const GET_USER_BY_ID_SUCCESS = 'GET_USER_BY_ID_SUCCESS'
export const IMPORT_PETITION_SUCCESS = 'IMPORT_PETITION_SUCCESS'

// ==========
// = Modals =
// ==========

export const showModal = (showingModal) => {
  return {
    type: SHOW_MODAL,
    showingModal
  }
}

export const hideModals = () => {
  return {
    type: SHOW_MODAL,
    showingModal: ''
  }
}

// ===========
// = Signers =
// ===========

export const getSignersSuccess = (signers) => {
  return {
    type: GET_SIGNERS_SUCCESS,
    signers
  }
}

export const getSigners = (id) => {
  return (dispatch, getState) => {
    return request(`petitions/${id}/signers`, {
      headers: {
        'Authorization': getState().authToken
      }
    })
      .then(json => dispatch(getSignersSuccess(json)))
      .catch(err => toastr.error('Fail to get signers', err))
  }
}


// =============
// = Petitions =
// =============

export const importPetitionSuccess = (id) => {
  return {
    type: IMPORT_PETITION_SUCCESS,
    id
  }
}

export const importPetition = (yaml, forwardError = false) => {
  return (dispatch, getState) => {
    return request(`/petitions/import`, {
      method: 'POST',
      headers: {
        'Authorization': getState().authToken
      },
      body: JSON.stringify({ petition: btoa(yaml) })
    })
      .then(json => {
        dispatch(importPetitionSuccess(json))
        return json.id
      })
      .catch(err => {
        toastr.error('Fail to import petition', err)
        if (forwardError)
          throw new Error(err)
      })
  }
}

export const signPetitionSuccess = (id) => {
  return {
    type: SIGN_PETITION_SUCCESS,
    id
  }
}

export const signPetition = (id) => {
  return (dispatch, getState) => {
    return request(`petitions/${id}/sign`, {
      method: 'POST',
      headers: {
        'Authorization': getState().authToken
      },
      body: JSON.stringify({ id: id })
    })
      .then(() => {
        dispatch(signPetitionSuccess(id))
      })
      .catch(err => {
        toastr.error('Fail to sign petition', err)
      })
  }
}

export const getPetitionSuccess = (petition) => {
  return {
    type: GET_PETITION_SUCCESS,
    petition
  }
}

export const getPetition = (id) => {
  return (dispatch, getState) => {
    return request(`petitions/${id}`, {
      headers: {
        'Authorization': getState().authToken
      },
    })
      .then(json => dispatch(getPetitionSuccess(json)))
      .catch(err => toastr.error('Fail to load petition', err))
  }
}

export const createPetitionSuccess = (id) => {
  return {
    type: CREATE_PETITION_SUCCESS,
    id
  }
}

export const createPetition = (petition) => {
  return (dispatch, getState) => {
    return request('petitions', {
      method: 'POST',
      headers: {
        'Authorization': getState().authToken
      },
      body: JSON.stringify(petition)
    })
      .then(json => {
        toastr.success('Petition successfully created')
        dispatch(createPetitionSuccess(json.id))
        return json.id
      })
      .catch(err => toastr.error('Petition creation failed', err))
  }
}

export const getPetitionsSuccess = (petitions, page) => {
  return {
    type: GET_PETITIONS_SUCCESS,
    petitions,
    page
  }
}

export const getPetitions = (query = {}) => {
  return (dispatch, getState) => {
    const q = queryString.stringify(query)

    return request(`petitions?${q}`, {
      headers: {
        'Authorization': getState().authToken
      }
    })
      .then(json => dispatch(getPetitionsSuccess(json, query.page)))
      .catch(err => toastr.error('Fail to load petitions', err))
  }
}

// ================
// = Registration =
// ================

export const signupSuccess = (authToken) => {
  return {
    type: SIGNUP_SUCCESS,
    authToken
  }
}

export const signup = (user) => {
  return dispatch => {

    return request('signup', {
      method: 'POST',
      body: JSON.stringify(user)
    })
      .then(json => {
        dispatch(signupSuccess(json.auth_token))
        toastr.success('Account created')
        dispatch(getUser())
      })
      .catch(err => toastr.error('Sign Up failed', err))
  }
}

// =================
// = Authorization =
// =================

export const logout = () => {
  return {
    type: LOGOUT
  }
}

export const loginSuccess = (authToken) => {
  return {
    type: LOGIN_SUCCESS,
    authToken
  }
}

export const login = (email, password) => {
  return dispatch => {
    return request('auth/login', {
      method: 'POST',
      body: JSON.stringify({
        email,
        password
      })
    })
      .then(json => {
        dispatch(loginSuccess(json.auth_token))
        dispatch(getUser())
      })
      .catch(err => toastr.error('Log In failed', err))
  }
}

// ========
// = User =
// ========

export const getUserSuccess = (user) => {
  return {
    type: GET_USER_SUCCESS,
    user
  }
}

export const getUser = (silent = false) => {
  return (dispatch, getState) => {
    return request('me', {
      headers: {
        'Authorization': getState().authToken
      }
    })
      .then(json => {
        dispatch(hideModals())
        dispatch(getUserSuccess(json))
      })
      .catch(err => {
        if (!silent)
          toastr.error('User load failed', err)
      })
  }
}

export const getUserByIdSuccess = (user) => {
  return {
    type: GET_USER_BY_ID_SUCCESS,
    user
  }
}

export const getUserById = (id) => {
  return dispatch => {
    return request(`users/${id}`)
      .then(json => dispatch(getUserByIdSuccess(json)))
      .catch(err => toastr.error('Fail to load user', err))
  }
}

// =========
// = Stats =
// =========

export const getStatsSuccess = (stats) => {
  return {
    type: GET_STATS_SUCCESS,
    stats
  }
}

export const getStats = () => {
  return dispatch => {
    return request('stats')
      .then(json => dispatch(getStatsSuccess(json)))
      .catch(err => toastr.error('Fail to load stats', err))
  }
}
