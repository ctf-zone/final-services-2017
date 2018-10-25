import 'babel-polyfill'
import React from 'react'
import ReactDOM from 'react-dom'
import { createStore, applyMiddleware } from 'redux'
import thunkMiddleware from 'redux-thunk'
import { createLogger } from 'redux-logger'
import createHistory from 'history/createBrowserHistory'
import { routerMiddleware } from 'react-router-redux'
import Root from './Root'
import rootReducer from './reducers'
import './index.css'

const history = createHistory()

let middlewares = [thunkMiddleware, routerMiddleware(history)]

if (process.env.NODE_ENV !== 'production') {
  middlewares.push(createLogger())
}

const store = createStore(
  rootReducer,
  { authToken: localStorage.getItem('authToken') },
  applyMiddleware(...middlewares)
)

store.subscribe(() => {
  localStorage.setItem('authToken', store.getState().authToken)
})

ReactDOM.render(
  <Root store={store} history={history} />,
  document.getElementById('root')
)
