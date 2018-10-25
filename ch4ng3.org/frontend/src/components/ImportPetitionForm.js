import React, { Component } from 'react'
import { connect } from 'react-redux'
import { push } from 'react-router-redux'
import {
  Header,
  Label
} from 'semantic-ui-react'
import { Form } from 'formsy-semantic-ui-react'
import { importPetition } from '../actions'

class NewPetitionForm extends Component {
  state = {
    canBeSubmitted: false,
    isLoading: false,
  }

  submit = ({ yaml }) => {
    const { dispatch } = this.props

    this.setState({ isLoading: true })

    dispatch(importPetition(yaml, true))
      .then(id => {
        this.setState({ isLoading: false })
        dispatch(push(`petition/${id}`))
      })
      .catch(err => this.setState({ isLoading: false }))
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
        <Header as='h1' content='Import petition' />
        <Form
          onValidSubmit={this.submit}
          onValid={this.enableSubmit}
          onInvalid={this.disableSubmit}>

          <Form.TextArea
            autoFocus
            required
            name='yaml'
            label='YAML'
            placeholder='YAML'
            validationErrors={{
              isDefaultRequiredValue: 'YAML is reqired',
            }}
            errorLabel={errorLabel} />

          <Form.Button
            disabled={!canBeSubmitted}
            loading={isLoading}
            color='red'>
            Import
          </Form.Button>

        </Form>
      </div>
    )
  }
}

export default connect()(NewPetitionForm)
