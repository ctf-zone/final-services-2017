import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Label, Icon } from 'semantic-ui-react'
import { Link } from 'react-router-dom'

class PetitionSignatures extends Component {

  render() {
    const { petition, user } = this.props

    const isAuthor = petition.user_id === user.id

    return (
      <span>
        { isAuthor ?
            <Label
              as={Link}
              to={`/user`}>
              <Icon
                color='blue'
                name='user' />
              <span style={{ 'color': '#2185d0' }}>
                you
              </span>
            </Label>
            :
            <Label
              as={Link}
              to={`/user/${petition.user_id}`}>
              <Icon
                name='user' />
              <span style={{ 'color': '#767676' }}>
                {petition.creator}
              </span>
            </Label>
        }
      </span>
    )
  }
}

const mapStateToProps = (state) => {
  const { user } = state
  return {
    user
  }
}

export default connect(mapStateToProps)(PetitionSignatures)
