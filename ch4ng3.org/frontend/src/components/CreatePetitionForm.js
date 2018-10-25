import React, { Component } from 'react'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'
import {
  Header,
  Label
} from 'semantic-ui-react'
import { Form } from 'formsy-semantic-ui-react'
import { createPetition } from '../actions'

class NewPetitionForm extends Component {
  state = {
    canBeSubmitted: false,
    isLoading: false,
  }

  submit = (petition) => {
    const { dispatch } = this.props

    this.setState({ isLoading: true })

    dispatch(createPetition(petition))
      .then(id => {
        this.setState({ isLoading: false })
        dispatch(push(`petition/${id}`))
      })
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

  render() {
    const { canBeSubmitted, isLoading } = this.state
    const errorLabel = <Label color='red' pointing/>

    return (
      <div className='new-petition'>
        <Header as='h1' content='New petition' />
        <Form
          onValidSubmit={this.submit}
          onValid={this.enableSubmit}
          onInvalid={this.disableSubmit}>

          <Form.Input
            autoFocus
            name='title'
            label='Title'
            placeholder='Title'
            required
            validations='minLength:4'
            validationErrors={{
              isDefaultRequiredValue: 'Title is reqired',
              minLength: 'Title minimum length is 4'
            }}
            errorLabel={errorLabel} />

          <Form.TextArea
            name='text'
            label='Text'
            placeholder='Text' />

          <Form.Button
            disabled={!canBeSubmitted}
            loading={isLoading}
            color='red'>
            Submit
          </Form.Button>

        </Form>
      </div>
    )
  }
}

export default connect()(NewPetitionForm)
