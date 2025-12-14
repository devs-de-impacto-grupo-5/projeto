import styled from 'styled-components';
import { Link } from 'react-router-dom';
import { darkPurple } from '../../constants/colors';

// Cores
const lightPurpleBg = '#D0C2E6'; 
const bgColor = '#F9FAF5';
const inputBorder = '#E0E0E0';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${bgColor};

  @media (min-width: 1024px) {
    display: grid;
    grid-template-columns: 1fr 1fr;
    height: 100vh;
  }
`;

export const BannerSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: ${lightPurpleBg};
  padding: 40px;
  
  @media (min-width: 1024px) {
    align-items: flex-start;
    padding: 0 100px;
    height: 100%;
  }
`;

export const LogoImage = styled.img`
  width: 120px;
  margin-bottom: 40px;

  @media (min-width: 1024px) {
    width: 160px;
  }
`;

export const WelcomeTitle = styled.h1`
  font-size: 24px;
  color: ${darkPurple};
  font-weight: 700;
  text-align: center;
  margin-bottom: 16px;
  font-family: 'Inter', sans-serif;

  @media (min-width: 1024px) {
    text-align: left;
    font-size: 40px;
    line-height: 1.2;
    max-width: 400px;
  }
`;

export const Slogan = styled.p`
  font-size: 16px;
  color: #4A4A4A;
  text-align: center;
  max-width: 300px;
  line-height: 1.6;
  font-family: 'Inter', sans-serif;

  @media (min-width: 1024px) {
    text-align: left;
    font-size: 18px;
    max-width: 400px;
  }
`;

export const FormSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px;
  flex: 1;
  background-color: ${bgColor};

  @media (min-width: 1024px) {
    align-items: flex-start;
    padding: 0 120px;
  }
`;

export const FormTitle = styled.h2`
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
  font-weight: 600;
  align-self: flex-start;
  width: 100%;
  font-family: 'Inter', sans-serif;
`;

export const FormSubtitle = styled.p`
  font-size: 14px;
  color: #666;
  margin-bottom: 32px;
  align-self: flex-start;
  font-family: 'Inter', sans-serif;
`;

export const InputGroup = styled.div`
  width: 100%;
  margin-bottom: 20px;
`;

export const Label = styled.label`
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
  font-family: 'Inter', sans-serif;
`;

export const InputWrapper = styled.div`
  display: flex;
  align-items: center;
  background-color: #FFFFFF;
  border: 1px solid ${inputBorder};
  border-radius: 8px;
  padding: 0 16px;
  height: 48px;
  transition: border-color 0.2s ease;

  &:focus-within {
    border-color: ${darkPurple};
    box-shadow: 0 0 0 2px rgba(106, 58, 159, 0.1);
  }

  svg {
    margin-right: 12px;
    color: #999;
  }
`;

export const Input = styled.input`
  border: none;
  background: transparent;
  flex: 1;
  height: 100%;
  font-size: 16px;
  color: #333;
  font-family: 'Inter', sans-serif;

  &::placeholder {
    color: #BBB;
  }

  &:focus {
    outline: none;
  }
`;

export const PrimaryButton = styled.button`
  width: 100%;
  height: 50px;
  background-color: ${darkPurple};
  color: #FFF;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 16px;
  font-family: 'Inter', sans-serif;

  &:hover {
    background-color: #582A8A;
  }
`;

export const Divider = styled.div`
  display: flex;
  align-items: center;
  width: 100%;
  margin: 24px 0;
  color: #999;
  font-size: 14px;
  font-family: 'Inter', sans-serif;

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: #E0E0E0;
  }

  &::before {
    margin-right: 16px;
  }

  &::after {
    margin-left: 16px;
  }
`;

export const SecondaryButton = styled(Link)`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 50px;
  background-color: transparent;
  color: ${darkPurple};
  border: 1px solid ${darkPurple};
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.2s;
  font-family: 'Inter', sans-serif;

  &:hover {
    background-color: rgba(106, 58, 159, 0.05);
  }
`;
