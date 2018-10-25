import React, { Component } from 'react'
import { connect } from 'react-redux'
import {
  Menu,
  Segment
} from 'semantic-ui-react'
import Profile from './Profile'
import PetitionsList from './PetitionsList'

class CurrentUser extends Component {

  state = { activeItem: 'profile' }

  switchTab = (e, { name }) => {
    this.setState({
      activeItem: name
    })
  }

  render() {
    const { user } = this.props
    const { activeItem } = this.state

    let segment
    switch (activeItem) {

      case 'profile':
        segment = (
          <Segment key='profile'>
            <Profile />
          </Segment>
        )
        break

      case 'created':
        segment = (
          <Segment key='created'>
            <PetitionsList
              filter={{ author_id: user.id }}
              emptyMessage="You haven't created any petitions yet" />
          </Segment>
        )
        break

      case 'signed':
        segment = (
          <Segment key='signed'>
            <PetitionsList
              filter={{ signer_id: user.id }}
              emptyMessage="You haven't signed any petition yet" />
          </Segment>
        )
        break
      default:
    }

    return (
      <div className='profile'>
        <Menu secondary pointing>
          <Menu.Item
            name='profile'
            active={activeItem === 'profile'}
            onClick={this.switchTab} />

          <Menu.Item
            name='created'
            active={activeItem === 'created'}
            onClick={this.switchTab}>
            Your petitions
          </Menu.Item>

          <Menu.Item
            name='signed'
            active={activeItem === 'signed'}
            onClick={this.switchTab}>
            Signed by you
          </Menu.Item>
        </Menu>

        {segment}
      </div>
    )
  }
}

function mapStateToProps(state) {
  const { user } = state
  return {
    user
  }
}

export default connect(mapStateToProps)(CurrentUser)
