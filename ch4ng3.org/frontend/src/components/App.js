import React, { Component } from 'react'
import { Container } from 'semantic-ui-react'
import { Route, withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import ReduxToastr from 'react-redux-toastr'
import { getUser } from '../actions'
import Nav from './Nav'
import Modals from './Modals'
import Home from './Home'
import Browse from './Browse'
import NewPetition from './NewPetition'
import CurrentUser from './CurrentUser'
import Petition from './Petition'
import User from './User'
import requireAuth from './requireAuth'

class App extends Component {
  componentDidMount() {
    const { dispatch, authToken } = this.props
    if (authToken) {
      dispatch(getUser(true))
    }
  }

  render() {
    return (
      <div>
        <ReduxToastr
          timeOut={4000}
          newestOnTop={false}
          preventDuplicates
          position='bottom-right'
          transitionIn='fadeIn'
          transitionOut='fadeOut'
          progressBar/>
        <Nav />
        <Modals />
        <Container style={{ padding: '50px' }}>
          <Route exact path='/' component={Home} />
          <Route exact path='/browse' component={Browse} />
          <Route exact path='/new' component={requireAuth(NewPetition)} />
          <Route exact path='/user' component={requireAuth(CurrentUser)} />
          <Route exact path='/user/:id' component={User} />
          <Route exact path='/petition/:id' component={Petition} />
        </Container>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  const { authToken } = state
  return {
    authToken
  }
}

export default withRouter(connect(mapStateToProps)(App))
