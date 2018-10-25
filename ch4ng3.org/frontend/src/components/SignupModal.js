import React, { Component } from 'react'
import { connect } from 'react-redux'
import {
  Modal,
  Button,
  Header,
  Label
} from 'semantic-ui-react'
import { Form } from 'formsy-semantic-ui-react'
import {
  hideModals,
  showModal,
  signup
} from '../actions'

class SignupModal extends Component {

  state = {
    canBeSubmitted: false,
    isLoading: false
  }

  closeModal = () => {
    const { dispatch } = this.props
    dispatch(hideModals())
  }

  submit = (user) => {
    const { dispatch } = this.props

    this.setState({ isLoading: true })

    dispatch(signup(user))
      .then(() => this.setState({ isLoading: false }))
  }

  enableSubmit = () => {
    this.setState({
      canBeSubmitted: true
    })
  }

  disableSubmit = () => {
    this.setState({
      canBeSubmitted: false
    })
  }

  openLoginModal = () => {
    const { dispatch } = this.props
    dispatch(showModal('login'))
  }

  render() {
    const { isShowing } = this.props
    const { isLoading, canBeSubmitted } = this.state
    const errorLabel = <Label color='red' pointing/>

      return (
        <Modal
          size='mini'
          open={isShowing}
          onClose={this.closeModal}
          closeIcon>

          <Modal.Header>
            <Header content='Sign Up' />
          </Modal.Header>

          <Modal.Content>

            <div style={{ marginBottom: '1em' }}>
              Already have an account? <a onClick={this.openLogInModal}>Log In</a>
            </div>

            <Form
              id='signup-form'
              onValidSubmit={this.submit}
              onValid={this.enableSubmit}
              onInvalid={this.disableSubmit}>

              <Form.Input
                autoFocus
                name='name'
                label='Name'
                placeholder='Name'
                required
                validations='minLength:3'
                validationErrors={{
                  isDefaultRequiredValue: 'Name is reqired',
                  minLength: 'Name minimum length is 3 characters'
                }}
                errorLabel={errorLabel} />

              <Form.Input
                name='phone'
                label='Phone'
                placeholder='Phone' />

              <Form.Input
                name='email'
                label='Email'
                placeholder='Email'
                required
                validations='isEmail'
                validationErrors={{
                  isDefaultRequiredValue: 'Email is reqired',
                  isEmail: 'Email is not valid'
                }}
                errorLabel={errorLabel} />

              <Form.Input
                name='password'
                label='Password'
                placeholder='Password'
                required
                type='password'
                validations='minLength:4'
                validationErrors={{
                  isDefaultRequiredValue: 'Password is reqired',
                  minLength: 'Name minimum length is 4 characters'
                }}
                errorLabel={errorLabel} />

            </Form>
          </Modal.Content>

          <Modal.Actions>
            <Button
              disabled={!canBeSubmitted}
              loading={isLoading}
              form='signup-form'
              type='submit'
              color='red'>
              Sign Up
            </Button>
          </Modal.Actions>

        </Modal>
      )
  }
}

const mapStateToProps = (state) => {
  const { showingModal } = state
  return {
    isShowing: showingModal === 'signup',
  }
}

export default connect(mapStateToProps)(SignupModal)
