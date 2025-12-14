import styled from 'styled-components';
import { neutral, lightGreen, lightPurple, darkPurple, lightYellow, darkYellow, darkGreen } from '../../constants/colors';
import { mediumSpacing, largeSpacing, baseSpacing } from '../../constants/spacing';

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: ${neutral};
  position: relative;
  overflow: hidden;
  padding: ${largeSpacing};
  font-family: 'Montserrat', sans-serif;
`;

export const TopShape = styled.img`
  position: absolute;
  top: 0;
  right: 0;
  width: 186px;
  height: 169px;
  z-index: 0;
  @media (min-width: 1024px) {
  @media (min-width: 1024px) {
    width: 300px;
    height: 280px;
    top: -40px;
    right: -40px;
  }
`;

export const BottomShape = styled.img`
  position: absolute;
  bottom: 50px;
  left: 0;
  width: 184px;
  height: 171px;
  z-index: 0;
  @media (min-width: 1024px) {
    width: 320px;
    height: 300px;
    bottom: -50px;
    left: -40px;
  }
`;

export const Header = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: ${largeSpacing};
  z-index: 1;
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
`;

export const UserInfo = styled.div`
  display: flex;
  align-items: center;
  gap: ${mediumSpacing};
`;

export const Avatar = styled.img`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  @media (min-width: 1024px) {
    width: 64px;
    height: 64px;
  }
`;

export const Greeting = styled.div`
  display: flex;
  flex-direction: column;
`;

export const GreetingText = styled.span`
  font-size: 14px;
  color: #666;
  @media (min-width: 1024px) {
    font-size: 16px;
  }
`;

export const UserName = styled.span`
  font-size: 18px;
  font-weight: bold;
  color: #333;
  @media (min-width: 1024px) {
    font-size: 20px;
  }
`;

export const SupportButton = styled.button`
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: ${lightYellow};
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: ${darkYellow};
  font-size: 24px;
  box-shadow: 0 4px 15px rgba(253, 215, 104, 0.4);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(253, 215, 104, 0.6);
    filter: brightness(1.05);
  }

  @media (min-width: 1024px) {
    width: 56px;
    height: 56px;
    font-size: 28px;
  }
`;

export const Content = styled.div`
  z-index: 1;
  flex: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
`;

export const Title = styled.h1`
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: ${baseSpacing};
  @media (min-width: 1024px) {
    font-size: 32px;
    margin-bottom: ${mediumSpacing};
  }
`;

export const Subtitle = styled.p`
  font-size: 16px;
  color: #666;
  margin-bottom: ${largeSpacing};
  @media (min-width: 1024px) {
    font-size: 18px;
    margin-bottom: 48px;
  }
`;

export const Grid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: ${mediumSpacing};
  @media (min-width: 1024px) {
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;
  }
`;

export const Card = styled.div`
  border-radius: 16px;
  aspect-ratio: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
  }
`;

export const SvgCard = styled.div`
  position: relative;
  width: 100%;
  aspect-ratio: 1;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 24px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);

  &:hover {
    transform: translateY(-8px);
  }

  /* Ensure content stays inside rounded corners */
  overflow: hidden; 

  @media (min-width: 1024px) {
    max-width: 100%;
    margin: 0 auto;
    border-radius: 32px;
  }
`;

export const SvgImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover; /* Ensure it covers the background nicely */
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.5s ease;
  
  ${SvgCard}:hover & {
    transform: scale(1.05);
  }

  @media (min-width: 1024px) {
    position: absolute; /* Revert to absolute to fill the card */
    width: 100%;
    height: 100%;
  }
`;

export const SvgCardTitle = styled.span`
  position: absolute;
  top: 24px;
  left: 24px;
  right: 24px;
  z-index: 2;
  font-size: 18px;
  font-weight: 700;
  color: #1A1A1A;
  max-width: calc(100% - 48px);
  word-wrap: break-word;
  line-height: 1.2;
  
  @media (min-width: 1024px) {
    font-size: 22px;
    top: 32px;
    left: 32px;
  }
`;

export const CardTitle = styled.span`
  font-size: 16px;
  font-weight: 600;
  color: #333;
`;

export const CardIcon = styled.div`
  align-self: flex-end;
  font-size: 40px;
  color: ${props => props.color || darkPurple};
  opacity: 0.8;
`;
