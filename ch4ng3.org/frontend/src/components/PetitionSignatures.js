import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Label, Icon, Popup } from 'semantic-ui-react'
import { signPetition } from '../actions'

class PetitionSignatures extends Component {

  signPetition = () => {
    const { dispatch, petition, isLoggedIn, onSign } = this.props

    if (isLoggedIn && !petition.already_signed) {
      dispatch(signPetition(petition.id))
        .then(() => {
          if (onSign) onSign()
        })
    }
  }

  render() {
    const { isLoggedIn, petition } = this.props

    const isSigned = isLoggedIn && petition.already_signed
    const canSign = isLoggedIn && !isSigned

    const popupText =
      !isLoggedIn ?
      'Login to sign the petition' :
      isSigned ?
      'You\'ve already signed this petition' :
      ''

    const signatures = (
      <Label
        onClick={this.signPetition}
        as={canSign ? 'a' : ''}>
        <Icon
          color={isSigned ? 'green' : 'grey'}
          name='check' />
        <span style={{ 'color': isSigned ? '#21ba45' : '#767676' }}>
          {petition.signature_count}
        </span>
      </Label>
    )

    return (
      <span>
        { canSign ?
            <span>
              {signatures}
            </span>
            :
            <Popup
              trigger={signatures}
              content={popupText}
              inverted
            />
        }
      </span>
    )
  }
}

const mapStateToProps = (state) => {
  const { user } = state
  return {
    isLoggedIn: user.id !== undefined
  }
}

export default connect(mapStateToProps)(PetitionSignatures)
