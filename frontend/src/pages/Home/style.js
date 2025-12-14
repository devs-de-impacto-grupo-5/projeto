import styled from 'styled-components';
import { darkPurple, darkYellow, lightGreen, neutral } from '../../constants/colors';
import { largeSpacing, mediumSpacing } from '../../constants/spacing';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px 40px;
  background: linear-gradient(135deg, ${neutral} 0%, #ffffff 100%);
  overflow-x: hidden;

  @media (min-width: 1024px) {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      "logo image"
      "slogan image"
      "question image"
      "buttons image"
      "link image";
    gap: 0px 60px;
    max-width: 1280px;
    margin: 0 auto;
    justify-items: start;
    align-content: center;
    padding: 0 60px;
  }
`;

export const LogoWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  width: 100%;

  @media (min-width: 1024px) {
    grid-area: logo;
    justify-content: flex-start;
    margin-bottom: ${mediumSpacing};
  }
`;

export const LogoImage = styled.img`
  width: 40%;
  max-width: 200px;
  
  @media (min-width: 1024px) {
    width: 220px;
  }
`;

export const Slogan = styled.h2`
  font-size: 20px;
  width: 80%;
  text-align: center;
  font-weight: 600;
  color: ${darkPurple};
  margin-bottom: ${largeSpacing};
  line-height: 1.4;

  @media (min-width: 1024px) {
    grid-area: slogan;
    text-align: left;
    font-size: 48px;
    width: 100%;
    max-width: 600px;
    margin-bottom: ${mediumSpacing};
  }
`;

export const ProdutorWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;
  height: 150px;
  background-color: ${lightGreen};
  border-radius: 50%;
  margin-bottom: ${largeSpacing};
  position: relative;
  transition: all 0.3s ease;

  @media (min-width: 1024px) {
    grid-area: image;
    width: 500px;
    height: 500px;
    margin-bottom: 0;
    /* Organic blob shape */
    border-radius: 42% 58% 70% 30% / 45% 45% 55% 55%;
    justify-self: center;
    box-shadow: 20px 20px 60px #d0d0c4, -20px -20px 60px #ffffff;
  }
`;

export const ProdutorImage = styled.img`
  width: 250px;
  height: auto;
  position: relative;
  z-index: 1;

  @media (min-width: 1024px) {
    width: 650px;
    /* Slightly offset the image for dynamic feel */
    transform: translate(-20px, -20px);
  }
`;

export const Question = styled.h3`
  font-size: 14px;
  color: ${darkPurple};
  text-align: center;
  width: 80%;
  font-weight: 700;
  margin-bottom: ${largeSpacing};

  @media (min-width: 1024px) {
    grid-area: question;
    text-align: left;
    font-size: 24px;
    width: 100%;
    margin-bottom: ${mediumSpacing};
  }
`;

export const ButtonsWrapper = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
  align-items: center;
  margin-bottom: ${largeSpacing};

  /* Ensure consistent sizing */
  & > a {
    width: 90%;
    max-width: 320px;
  }

  @media (min-width: 1024px) {
    grid-area: buttons;
    flex-direction: row;
    justify-content: flex-start;
    align-items: stretch; /* Ensure same height */
    width: auto;
    gap: 24px;

    & > a {
      width: 280px; /* Ensure same width */
      max-width: none;
    }
  }
`;

export const ChangeAccountType = styled.small`
  color: ${darkYellow};
  text-align: center;
  width: 100%;
  cursor: pointer;
  
  &:hover {
    text-decoration: underline;
  }

  @media (min-width: 1024px) {
    grid-area: link;
    text-align: left;
    font-size: 16px;
    margin-top: ${mediumSpacing};
  }
`;