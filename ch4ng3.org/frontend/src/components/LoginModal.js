import React, { Component } from 'react'
import { connect } from 'react-redux'
import {
  Modal,
  Button,
  Header,
  Label,
} from 'semantic-ui-react'
import { Form } from 'formsy-semantic-ui-react'
import {
  hideModals,
  showModal,
  login
} from '../actions'

class LoginModal extends Component {
  state = {
    canBeSubmitted: false,
    isLoading: false
  }

  closeModal = () => {
    const { dispatch } = this.props
    dispatch(hideModals())
  }

  submit = ({ email, password }) => {
    const { dispatch } = this.props

    this.setState({ isLoading: true })

    dispatch(login(email, password))
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

  openSignUpModal = () => {
    const { dispatch } = this.props
    dispatch(showModal('signup'))
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
          <Header content='Log In' />
        </Modal.Header>
        <Modal.Content>
          <div style={{ marginBottom: '1em' }}>
            Don't have an account? <a onClick={this.openSignUpModal}>Sign Up</a>
          </div>

          <Form
            onValidSubmit={this.submit}
            onValid={this.enableSubmit}
            onInvalid={this.disableSubmit}
            id='login-form'>

            <Form.Input
              autoFocus
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
              type='password'
              required
              validationErrors={{
                isDefaultRequiredValue: 'Password is reqired'
              }}
              errorLabel={errorLabel} />

          </Form>

        </Modal.Content>

        <Modal.Actions>
          <Button
            disabled={!canBeSubmitted}
            loading={isLoading}
            form='login-form'
            type='submit'
            color='red'>
            Log In
          </Button>

        </Modal.Actions>
      </Modal>
    )
  }
}

const mapStateToProps = (state) => {
  const { showingModal } = state

  return {
    isShowing: showingModal === 'login',
  }
}

export default connect(mapStateToProps)(LoginModal)
