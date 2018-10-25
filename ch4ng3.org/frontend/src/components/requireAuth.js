import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

const requireAuth = (Wrapped) => {
  class AuthenticatedComponent extends Component {

    static propTypes = {
      isLoggedIn: PropTypes.bool.isRequired,
    }

    render() {
      const { isLoggedIn } = this.props
      if (!isLoggedIn) {
        return <h1>Your are not logged in</h1>
      }
      return <Wrapped {...this.props} />
    }
  }

  const mapStateToProps = (state) => {
    const { user } = state
    return {
      isLoggedIn: user.name !== undefined
    }
  }

  return connect(mapStateToProps)(AuthenticatedComponent)
}

export default requireAuth
