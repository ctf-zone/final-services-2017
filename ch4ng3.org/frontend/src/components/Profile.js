import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Icon, Segment } from 'semantic-ui-react'
import './Profile.css'

class Profile extends Component {

  static defaultProps = {
    user: {}
  }

  render() {
    const { user } = this.props

    return (
      <Segment
        basic={true}
        loading={user.name === undefined}>
        <div className='row name'>
          <Icon
            inverted
            circular
            color='red'
            name='user' />
          <span className='content'>{user.name}</span>
        </div>
        <div className='row email'>
          <Icon
            inverted
            circular
            color='red'
            name='mail' />
          <span className='content'>{user.email}</span>
        </div>
        <div className='row phone'>
          <Icon
            inverted
            circular
            color='red'
            name='phone' />
          <span className='content'>{ user.phone ? user.phone : '-' }</span>
        </div>
      </Segment>
    )
  }
}

const mapStateToProps = (state) => {
  const { user } = state
  return {
    user
  }
}

export default connect(mapStateToProps)(Profile)
