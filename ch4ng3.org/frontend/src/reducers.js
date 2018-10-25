import { combineReducers } from 'redux'
import { reducer as toastrReducer } from 'react-redux-toastr'
import { routerReducer } from 'react-router-redux'
import {
  SHOW_MODAL,
  LOGIN_SUCCESS,
  SIGNUP_SUCCESS,
  GET_USER_SUCCESS,
  LOGOUT,
  GET_PETITIONS_SUCCESS,
  SIGN_PETITION_SUCCESS,
  GET_PETITION_SUCCESS,
  GET_SIGNERS_SUCCESS,
  GET_STATS_SUCCESS,
  GET_USER_BY_ID_SUCCESS,
} from './actions'

const showingModal = (state = '', action) => {
  switch (action.type) {
    case SHOW_MODAL:
      return action.showingModal
    default:
      return state
  }
}

const authToken = (state = '', action) => {
  switch (action.type) {
    case LOGIN_SUCCESS:
    case SIGNUP_SUCCESS:
      return action.authToken
    case LOGOUT:
      return ''
    default:
      return state
  }
}

const user = (state = {}, action) => {
  switch (action.type) {
    case GET_USER_SUCCESS:
      return action.user
    case LOGOUT:
      return {}
    default:
      return state
  }
}

const petitions = (state = [], action) => {
  switch (action.type) {
    case GET_PETITIONS_SUCCESS:
      if (action.page)
        return [...state, ...action.petitions]
      else
        return action.petitions
    case SIGN_PETITION_SUCCESS:
      return state.map(petition =>
        (petition.id === action.id) ?
        {
          ...petition,
          already_signed: true,
          signature_count: petition.signature_count + 1
        }
        :
        petition
      )
    default:
      return state
  }
}

const petition = (state = {}, action) => {
  switch (action.type) {
    case SIGN_PETITION_SUCCESS:
      if (action.id === state.id) {
        return {
          ...state,
          already_signed: true,
          signature_count: state.signature_count + 1
        }
      } else
        return state
    case GET_PETITION_SUCCESS:
      return action.petition
    default:
      return state
  }
}

const signers = (state = [], action) => {
  switch (action.type) {
    case GET_SIGNERS_SUCCESS:
      return action.signers
    default:
      return state
  }
}

const stats = (state = {}, action) => {
  switch (action.type) {
    case GET_STATS_SUCCESS:
      return action.stats
    default:
      return state
  }
}

const users = (state = {}, action) => {
  switch (action.type) {
    case GET_USER_BY_ID_SUCCESS:
      return action.user
    default:
      return state
  }
}

const rootReducer = combineReducers({
  routerReducer,
  toastr: toastrReducer,
  showingModal,
  authToken,
  user,
  users,
  petitions,
  petition,
  signers,
  stats
})

export default rootReducer
