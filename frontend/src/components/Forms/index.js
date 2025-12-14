import React from 'react';
import { FormContainer, InputGroup, Label, Input } from './style';

const Forms = ({ fields }) => {
  return (
    <FormContainer>
      {fields.map((field, index) => (
        <InputGroup key={index}>
          {field.label && <Label>{field.label}</Label>}
          <Input
            type={field.type || 'text'}
            placeholder={field.placeholder || ''}
            value={field.value || ''}
            onChange={field.onChange}
            name={field.name}
            required={field.required || false}
          />
        </InputGroup>
      ))}
    </FormContainer>
  );
};

export default Forms;
